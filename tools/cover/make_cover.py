"""책 표지(docs/assets/cover.svg)를 만듭니다. 실행: python3 tools/cover/make_cover.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "figures"))
from lib import FONT  # noqa: E402

W, H = 900, 1260
CX, CY, R = 450, 600, 300
DIE = 38


def dies():
    out = []
    n = int(R / DIE) + 1
    for i in range(-n, n):
        for j in range(-n, n):
            x, y = CX + i * DIE, CY + j * DIE
            corners = [(x, y), (x + DIE, y), (x, y + DIE), (x + DIE, y + DIE)]
            if all(math.hypot(px - CX, py - CY) < R - 10 for px, py in corners):
                out.append((i, j, x, y))
    return out


def main():
    cells = []
    for i, j, x, y in dies():
        lit = (i, j) == (1, -2)
        warm = (i + j) % 7 == 0 and not lit
        fill = "url(#lit)" if lit else ("#2d4f8a" if warm else "#1d3866")
        cells.append(f'<rect x="{x + 2}" y="{y + 2}" width="{DIE - 4}" height="{DIE - 4}" rx="2" fill="{fill}"'
                     + (' filter="url(#glow)"' if lit else "") + "/>")
    lx, ly = CX + 1 * DIE + DIE / 2, CY - 2 * DIE + DIE / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="웨이퍼 위에 꿈을 새기다 표지" font-family="{FONT}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1633"/><stop offset="1" stop-color="#14306b"/></linearGradient>
  <radialGradient id="wafer" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#8fb4e8"/><stop offset="0.55" stop-color="#3d64a8"/><stop offset="1" stop-color="#1c3260"/></radialGradient>
  <radialGradient id="lit" cx="0.5" cy="0.5" r="0.6"><stop offset="0" stop-color="#fff6c8"/><stop offset="1" stop-color="#ffc23d"/></radialGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffd35c" stop-opacity="0.55"/><stop offset="1" stop-color="#ffd35c" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="clip"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g fill="#ffffff" opacity="0.5">
  <circle cx="120" cy="140" r="1.6"/><circle cx="780" cy="110" r="1.2"/><circle cx="690" cy="230" r="1.8"/><circle cx="210" cy="260" r="1"/>
  <circle cx="820" cy="420" r="1.4"/><circle cx="70" cy="520" r="1.2"/><circle cx="840" cy="760" r="1"/><circle cx="90" cy="860" r="1.6"/>
</g>
<text x="{W / 2}" y="120" text-anchor="middle" font-size="22" fill="#9db6dd" letter-spacing="6">SAMSUNG DS CAREER GUIDE · UNOFFICIAL</text>
<circle cx="{CX}" cy="{CY}" r="{R + 14}" fill="none" stroke="#5f86c6" stroke-opacity="0.35" stroke-width="2"/>
<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#wafer)"/>
<g clip-path="url(#clip)">{"".join(cells)}</g>
<path d="M{CX - 14} {CY + R - 1} a14 14 0 0 0 28 0 z" fill="#0f2048"/>
<circle cx="{lx}" cy="{ly}" r="90" fill="url(#halo)"/>
<path d="M{lx} {ly - 6} C {lx + 60} {ly - 120}, {lx + 150} {ly - 170}, {lx + 230} {ly - 300}" fill="none" stroke="#ffd35c" stroke-width="2.5" stroke-dasharray="2 10" stroke-linecap="round" opacity="0.85"/>
<path d="M{lx + 230} {ly - 318} l6 14 15 2 -11 10 3 15 -13 -8 -13 8 3 -15 -11 -10 15 -2 z" fill="#ffe08a"/>
<text x="{W / 2}" y="1010" text-anchor="middle" font-size="70" font-weight="bold" fill="#ffffff">웨이퍼 위에 꿈을 새기다</text>
<rect x="{W / 2 - 40}" y="1046" width="80" height="4" rx="2" fill="#ffc23d"/>
<text x="{W / 2}" y="1102" text-anchor="middle" font-size="30" fill="#d6e2f5">삼성전자 DS부문 신입·경력 지원 가이드</text>
<text x="{W / 2}" y="1150" text-anchor="middle" font-size="24" fill="#9db6dd">반도체에 관심 있는 대학생과 취업준비생을 위하여</text>
<text x="{W / 2}" y="1220" text-anchor="middle" font-size="18" fill="#6f8bb8">비공식 가이드 · 삼성전자와 관련이 없습니다</text>
</svg>
'''
    out = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "assets", "cover.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
