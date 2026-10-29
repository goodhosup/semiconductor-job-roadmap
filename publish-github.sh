#!/usr/bin/env bash
# GitHub 저장소를 만들고 GitHub Pages로 책을 배포합니다.
# 사용법: bash publish-github.sh [저장소이름]
set -euo pipefail
cd "$(dirname "$0")"
REPO="${1:-semiconductor-job-roadmap}"

gh auth status >/dev/null || { echo "먼저 'gh auth login'을 실행하세요."; exit 1; }
LOGIN="$(gh api user -q .login)"

mkdir -p .github/workflows
cat > .github/workflows/deploy.yml <<'YML'
name: Deploy book to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
YML

sed -i.bak \
  -e '/^# 저장소를 만든 뒤/d' \
  -e "s|^# site_url: .*|site_url: https://${LOGIN}.github.io/${REPO}/|" \
  -e "s|^# repo_url: .*|repo_url: https://github.com/${LOGIN}/${REPO}|" \
  mkdocs.yml && rm -f mkdocs.yml.bak

[ -d .git ] || git init -b main
git add -A
git commit -m "Initial book: 반도체 직무 로드맵" || true
gh repo create "$REPO" --public --source=. --push \
  --description "반도체 직무 로드맵: 삼성전자 DS부문 신입·경력 지원 가이드 (비공식)"

gh api -X POST "repos/${LOGIN}/${REPO}/pages" -f build_type=workflow >/dev/null 2>&1 \
  || gh api -X PUT "repos/${LOGIN}/${REPO}/pages" -f build_type=workflow >/dev/null
gh workflow run deploy.yml -R "${LOGIN}/${REPO}" || true

echo "저장소: https://github.com/${LOGIN}/${REPO}"
echo "책 주소: https://${LOGIN}.github.io/${REPO}/ (배포까지 1~2분)"
echo "진행 상황: gh run watch -R ${LOGIN}/${REPO}"
