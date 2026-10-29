# 책 도식용 SVG 헬퍼. 모든 그림은 흰 카드 배경이라 라이트/다크 모드와 위키독스에서 똑같이 보인다.
from xml.sax.saxutils import escape as E
FONT="'Pretendard','Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif"
C=dict(ink="#1f2937",sub="#4b5563",line="#9ca3af",bg="#ffffff",card="#f8fafc",
       blue="#2563eb",blue_l="#dbeafe",green="#059669",green_l="#d1fae5",
       orange="#d97706",orange_l="#fef3c7",purple="#7c3aed",purple_l="#ede9fe",
       red="#dc2626",red_l="#fee2e2",gray_l="#e5e7eb",teal="#0d9488",teal_l="#ccfbf1")
class S:
    def __init__(s,w,h,title):
        s.w,s.h,s.t=w,h,title; s.o=[]
    def add(s,x): s.o.append(x); return s
    def rect(s,x,y,w,h,fill=C["card"],stroke=C["line"],r=10,sw=1.5,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        return s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(s,x,y,t,size=15,fill=C["ink"],anchor="middle",weight=400):
        lines=t.split("\n"); out=[]
        y0=y-(len(lines)-1)*size*0.62
        for i,l in enumerate(lines):
            out.append(f'<text x="{x}" y="{y0+i*size*1.25:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" dominant-baseline="middle">{E(l)}</text>')
        return s.add("".join(out))
    def box(s,x,y,w,h,label,fill=C["blue_l"],stroke=C["blue"],size=15,weight=600,sub=None,r=10):
        s.rect(x,y,w,h,fill,stroke,r)
        if sub:
            s.text(x+w/2,y+h/2-9,label,size,C["ink"],weight=weight)
            s.text(x+w/2,y+h/2+13,sub,size-3,C["sub"])
        else: s.text(x+w/2,y+h/2,label,size,C["ink"],weight=weight)
        return s
    def arrow(s,x1,y1,x2,y2,color=C["sub"],sw=2,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        return s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" marker-end="url(#ah)"{d}/>')
    def path(s,d,color=C["sub"],sw=2,arrow=True,dash=None,fill="none"):
        a=' marker-end="url(#ah)"' if arrow else ""; ds=f' stroke-dasharray="{dash}"' if dash else ""
        return s.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{a}{ds}/>')
    def line(s,x1,y1,x2,y2,color=C["ink"],sw=2):
        return s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')
    def heading(s,t,sub=None):
        s.text(24,30,t,19,C["ink"],"start",700)
        if sub: s.text(24,56,sub,13,C["sub"],"start")
        return s
    def save(s,path):
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}" role="img" aria-label="{E(s.t)}" font-family="{FONT}">
<title>{E(s.t)}</title>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{C['sub']}"/></marker></defs>
<rect x="0.5" y="0.5" width="{s.w-1}" height="{s.h-1}" rx="14" fill="{C['bg']}" stroke="{C['gray_l']}"/>
{chr(10).join(s.o)}
</svg>
'''
        open(path,"w").write(svg)
