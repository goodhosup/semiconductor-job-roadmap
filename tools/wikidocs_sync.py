#!/usr/bin/env python3
"""docs/의 원고를 위키독스(wikidocs.net) 책으로 올리거나 갱신합니다.

사용법 (저장소 루트에서):
    python3 tools/wikidocs_sync.py            # 토큰을 물어본 뒤 업로드
    python3 tools/wikidocs_sync.py --dry-run  # 네트워크 없이 변환 결과만 확인

- 토큰은 https://wikidocs.net/profile/edit/token 에서 발급합니다.
  환경변수 WIKIDOCS_TOKEN이 있으면 그것을 쓰고, 없으면 입력을 받습니다(화면에 표시되지 않음).
- 처음 실행하면 책을 새로 만들고, 페이지 번호를 tools/wikidocs/map.json에 저장합니다.
  다음 실행부터는 같은 페이지를 수정하므로, map.json은 저장소에 커밋해 두세요.
- 목차 순서는 mkdocs.yml의 nav를 따릅니다. 그림은 tools/wikidocs/png/의 PNG를 올립니다.
"""
import argparse
import getpass
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

try:
    import yaml
except ImportError:
    sys.exit("PyYAML이 필요합니다: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
STATE_DIR = os.path.join(ROOT, "tools", "wikidocs")
MAP_PATH = os.path.join(STATE_DIR, "map.json")
PNG_DIR = os.path.join(STATE_DIR, "png")
API = "https://wikidocs.net/napi"

LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")


class Api:
    def __init__(self, token, dry_run):
        self.token, self.dry, self.fake_id = token, dry_run, 900000

    def _req(self, method, path, body=None, files=None, fatal=True):
        if self.dry:
            self.fake_id += 1
            return {"id": self.fake_id, "image_url": f"https://wikidocs.net/images/page/dry/{self.fake_id}.png"}
        headers = {"Authorization": f"Token {self.token}"}
        data = None
        if files is not None:
            boundary = uuid.uuid4().hex
            parts = []
            for k, v in (body or {}).items():
                parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
            for k, (name, content, ctype) in files.items():
                parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\n'
                             f"Content-Type: {ctype}\r\n\r\n".encode() + content + b"\r\n")
            parts.append(f"--{boundary}--\r\n".encode())
            data = b"".join(parts)
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        elif body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    time.sleep(0.3)
                    text = r.read().decode()
                    return json.loads(text) if text else {}
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:300]
                if e.code == 401:
                    sys.exit("토큰이 올바르지 않습니다(401). 위키독스에서 토큰을 다시 확인하세요.")
                if not fatal:
                    return None
                if e.code in (429, 500, 502, 503) and attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue
                sys.exit(f"{method} {path} 실패: HTTP {e.code} {msg}")

    def me(self):
        return self._req("GET", "/auth/me/")

    def create_book(self, subject, summary):
        res = self._req("POST", "/books/create/", {"subject": subject, "summary": summary, "open_yn": "Y", "book_type": "B"}, files={})
        # 응답 스키마가 명시돼 있지 않아, id가 없으면 내 책 목록에서 같은 제목을 찾습니다.
        book_id = res.get("id") or res.get("book_id")
        if not book_id and not self.dry:
            found = [b["id"] for b in self._req("GET", "/books/") if b.get("subject") == subject]
            book_id = max(found) if found else None
        if not book_id:
            sys.exit(f"책 생성 응답에서 번호를 찾지 못했습니다: {res}")
        return {"id": book_id}

    def update_book(self, book_id, summary):
        """책 소개를 바꿉니다. 실패해도 멈추지 않고 None을 돌려줍니다."""
        return self._req("PATCH", f"/books/{book_id}/", {"summary": summary}, fatal=False)

    def create_page(self, book_id, parent_id, subject, content):
        return self._req("POST", "/pages/create/", {"subject": subject, "content": content, "parent_id": parent_id,
                                                    "book_id": book_id, "open_yn": "Y"})

    def patch_page(self, page_id, **fields):
        return self._req("PATCH", f"/pages/{page_id}/", fields)

    def upload_image(self, page_id, path):
        with open(path, "rb") as f:
            content = f.read()
        return self._req("POST", "/images/upload/", {"page_id": page_id},
                         files={"file": (os.path.basename(path), content, "image/png")})


def load_map():
    if os.path.exists(MAP_PATH):
        with open(MAP_PATH) as f:
            return json.load(f)
    return {"book_id": None, "pages": {}, "images": {}}


def save_map(m, dry):
    if dry:
        return
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(MAP_PATH, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=2, sort_keys=True)


def read_doc(rel):
    with open(os.path.join(DOCS, rel), encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"#\s+(.+)\n+", text)
    if m:
        return m.group(1).strip(), text[m.end():]
    return os.path.splitext(os.path.basename(rel))[0], text


def flatten_nav(nav):
    """nav를 (key, 제목, md경로 또는 None, 부모 key) 목록으로 바꿉니다. 부모가 먼저 나옵니다."""
    out = []

    def walk(items, parent):
        for item in items:
            if isinstance(item, str):
                out.append((item, None, item, parent))
            else:
                (title, val), = item.items()
                if isinstance(val, str):
                    out.append((val, title, val, parent))
                else:
                    first = val[0] if val and isinstance(val[0], str) and val[0].endswith("index.md") else None
                    if first:
                        out.append((first, title, first, parent))
                        walk(val[1:], first)
                    else:
                        key = "section:" + (parent or "") + "/" + title
                        out.append((key, title, None, parent))
                        walk(val, key)
    walk(nav, None)
    return out


def convert(rel, body, pages, images, api, page_id, dry):
    """상대 링크를 위키독스 페이지 주소로, 그림을 업로드한 PNG 주소로 바꿉니다."""
    base = os.path.dirname(rel)

    def repl(m):
        bang, text, target = m.groups()
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            return m.group(0)
        path, _, _anchor = target.partition("#")
        norm = os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")
        if bang:
            name = os.path.splitext(os.path.basename(norm))[0] + ".png"
            png = os.path.join(PNG_DIR, name)
            if not os.path.exists(png):
                print(f"  ! PNG 없음: {png} (tools/wikidocs/png를 먼저 만드세요)")
                return m.group(0)
            with open(png, "rb") as f:
                digest = hashlib.sha1(f.read()).hexdigest()[:12]
            cached = images.get(name)
            if not cached or cached["sha"] != digest:
                url = api.upload_image(page_id, png)["image_url"]
                images[name] = {"sha": digest, "url": url}
            return f"![{text}]({images[name]['url']})"
        if norm in pages:
            return f"[{text}](https://wikidocs.net/{pages[norm]})"
        if not norm.endswith(".md"):
            return m.group(0)
        print(f"  ! 연결할 페이지 없음: {rel} → {target}")
        return text

    # MkDocs 전용 속성({ width="..." })은 위키독스에서 글자로 보이므로 지웁니다.
    body = re.sub(r"(!\[[^\]]*\]\([^)]+\))\{[^}]*\}", r"\1", body)
    return LINK_RE.sub(repl, body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="네트워크 없이 변환 결과를 tools/wikidocs/preview/에 저장")
    args = ap.parse_args()

    with open(os.path.join(ROOT, "mkdocs.yml"), encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    token = "dry-run"
    if not args.dry_run:
        token = os.environ.get("WIKIDOCS_TOKEN") or getpass.getpass("위키독스 API 토큰: ").strip()
    api = Api(token, args.dry_run)
    if not args.dry_run:
        me = api.me()
        print(f"로그인 확인: {me.get('username') or me.get('name') or me}")

    m = load_map()
    if not m["book_id"]:
        m["book_id"] = api.create_book(cfg["site_name"], cfg.get("site_description", ""))["id"]
        print(f"책을 새로 만들었습니다: https://wikidocs.net/book/{m['book_id']}")
        save_map(m, args.dry_run)
    elif not args.dry_run:
        if api.update_book(m["book_id"], cfg.get("site_description", "")) is None:
            print("! 책 소개를 바꾸지 못했습니다. 위키독스 책 설정에서 직접 바꿔 주세요.")
        else:
            print("= 책 소개 갱신")

    entries = flatten_nav(cfg["nav"])
    titles = {}
    # 위키독스는 형제 페이지를 제목순으로 정렬하므로, 목차 순서대로 "01.", "01-02." 번호를 붙입니다.
    numbers, seen = {}, {}
    for key, _, _, parent in entries:
        seen[parent] = seen.get(parent, 0) + 1
        numbers[key] = (numbers[parent] + "-" if parent else "") + f"{seen[parent]:02d}"
    # 1단계: 없는 페이지를 목차 순서대로 만들어 번호를 확보합니다.
    for key, title, rel, parent in entries:
        subject = f"{numbers[key]}. " + (title or read_doc(rel)[0])
        titles[key] = subject
        if key not in m["pages"]:
            pid = api.create_page(m["book_id"], m["pages"].get(parent), subject, "작성 중입니다.")["id"]
            m["pages"][key] = pid
            save_map(m, args.dry_run)
            print(f"+ 페이지 생성: {subject} ({pid})")

    # 2단계: 본문을 변환해 채웁니다.
    preview = os.path.join(STATE_DIR, "preview")
    for key, title, rel, parent in entries:
        pid = m["pages"][key]
        if rel:
            subject = titles[key]
            body = convert(rel, read_doc(rel)[1], m["pages"], m["images"], api, pid, args.dry_run)
        else:
            subject = titles[key]
            kids = [k for k, _, _, p in entries if p == key]
            body = "\n".join(f"- [{titles[k]}](https://wikidocs.net/{m['pages'][k]})" for k in kids) + "\n"
        if args.dry_run:
            os.makedirs(preview, exist_ok=True)
            name = re.sub(r"[^0-9A-Za-z가-힣_-]+", "_", key) + ".md"
            with open(os.path.join(preview, name), "w", encoding="utf-8") as f:
                f.write(f"<!-- parent={m['pages'].get(parent)} id={pid} -->\n# {subject}\n\n{body}")
        else:
            api.patch_page(pid, subject=subject, content=body, parent_id=m["pages"].get(parent), open_yn="Y")
            save_map(m, args.dry_run)
            print(f"= 본문 갱신: {subject}")

    print(f"\n완료. 책 주소: https://wikidocs.net/book/{m['book_id']}")
    if not args.dry_run:
        print("tools/wikidocs/map.json을 커밋해 두면 다음 실행 때 같은 페이지를 수정합니다.")


if __name__ == "__main__":
    main()
