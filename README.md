# 반도체 직무 로드맵

삼성전자 DS부문 취업 준비 가이드 (비공식)

공식 채용 사이트(samsung-dsrecruit.com)의 사업부·직무 정보를 바탕으로, 직무별 **공부 전략과 학습 로드맵**을 정리하는 책입니다.

## 로컬에서 보기

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve        # http://127.0.0.1:8000
```

## GitHub Pages로 발행하기

1. GitHub에 새 저장소를 만들고 이 폴더를 push 합니다.
2. 저장소 Settings → Pages → Source를 **GitHub Actions**로 바꿉니다.
3. `main`에 push 할 때마다 `.github/workflows/deploy.yml`이 책을 빌드해 배포합니다.
4. `mkdocs.yml`의 `site_url`, `repo_url` 주석을 풀고 실제 주소를 넣습니다.

## 위키독스로 발행하기

원고는 `docs/` 하나만 고칩니다. 위키독스에는 `mkdocs.yml`의 `nav` 순서대로 페이지를 만들고 각 `.md` 내용을 붙여넣습니다.
위키독스와 호환되도록 MkDocs 전용 문법(`!!!` 박스, 탭)은 쓰지 않습니다. 장끼리 연결하는 상대 링크는 위키독스에서 페이지 링크로 바꿔야 합니다.

## 새 장 쓰기

- 직무 장: `templates/job-chapter.md`를 복사해서 씁니다. 샘플: `docs/02-jobs/design/circuit-design.md`
- 사업부 장: `templates/division-chapter.md`를 복사해서 씁니다. 샘플: `docs/01-divisions/memory.md`
- 공식 사이트 문장은 복사하지 않고 직접 다시 씁니다. 각 장 상단에 확인 기준일을 적습니다.

## 그림 고치기

책의 도식은 모두 직접 만든 SVG이며 `docs/assets/figures/`에 있습니다. 그림을 고치려면 `tools/figures/figs.py`를 수정한 뒤 아래 명령으로 다시 만드세요.

```bash
python3 tools/figures/figs.py docs/assets/figures
```

위키독스에 올릴 때는 같은 SVG 파일을 각 페이지에 이미지로 업로드하면 됩니다.
