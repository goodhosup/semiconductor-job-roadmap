# 웨이퍼 위에 꿈을 새기다

삼성전자 DS부문 신입·경력 지원 가이드 (비공식)

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

`tools/wikidocs_sync.py`가 `docs/` 원고를 위키독스 책으로 올리고, 다음부터는 같은 페이지를 수정합니다.

1. https://wikidocs.net/profile/edit/token 에서 API 토큰을 발급합니다.
2. 저장소 루트에서 실행합니다. 토큰을 물어보면 붙여넣습니다(화면에 표시되지 않음).
   ```bash
   python3 tools/wikidocs_sync.py
   ```
3. 생성된 `tools/wikidocs/map.json`을 커밋합니다. 이 파일이 있어야 다음 실행 때 같은 페이지를 수정합니다.

- 목차 순서는 `mkdocs.yml`의 `nav`를 따르고, 장끼리의 링크는 위키독스 페이지 주소로 바뀝니다.
- 그림은 `tools/wikidocs/png/`의 PNG를 올립니다. 도식을 고쳤다면 `node tools/figures/svg2png.js docs/assets/figures tools/wikidocs/png`로 PNG도 다시 만드세요(Playwright 필요).
- 올리기 전에 `python3 tools/wikidocs_sync.py --dry-run`으로 변환 결과를 `tools/wikidocs/preview/`에서 확인할 수 있습니다.

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
