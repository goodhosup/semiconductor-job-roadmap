import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import S, C
OUT=sys.argv[1]; os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n)

# 1. 반도체 가치사슬
s=S(880,300,"반도체가 만들어지는 흐름과 DS부문 조직")
s.heading("반도체가 만들어지는 흐름","단계마다 주로 맡는 조직")
steps=[("설계","회로·칩 구조"),("마스크","패턴 원판"),("전공정","웨이퍼 위 회로"),("EDS","웨이퍼 검사"),("패키지","조립·보호"),("최종 테스트","출하 전 검사")]
w,g,x0,y=118,26,24,90
for i,(a,b) in enumerate(steps):
    x=x0+i*(w+g); s.box(x,y,w,70,a,sub=b)
    if i<len(steps)-1: s.arrow(x+w+2,y+35,x+w+g-2,y+35)
orgs=[(0,0,"메모리·S.LSI\nSAIT",C["purple_l"],C["purple"]),(1,3,"메모리 · Foundry · CTO 반도체연구소",C["green_l"],C["green"]),(4,5,"TSP총괄",C["orange_l"],C["orange"])]
for a,b,t,f,st in orgs:
    xa=x0+a*(w+g); xb=x0+b*(w+g)+w
    s.rect(xa,185,xb-xa,44,f,st,8); s.text((xa+xb)/2,207,t,12 if a==b else 13,C["ink"],weight=600)
s.rect(x0,242,6*w+5*g,40,C["teal_l"],C["teal"],8)
s.text(x0+(6*w+5*g)/2,262,"모든 단계를 받치는 기반: 글로벌 제조&인프라총괄(전력·물·가스·안전) · AX/PI센터(AI·IT)",13,C["ink"],weight=600)
s.save(P("overview-value-chain.svg"))

# 2. 8대 공정
s=S(880,270,"반도체 8대 공정")
s.heading("반도체 8대 공정","1~6은 전공정(팹), 7~8은 검사와 후공정")
steps=["웨이퍼 제조","산화","포토(노광)","식각","증착·이온주입","금속 배선","EDS 검사","패키징"]
w,h,g=190,58,22
for i,t in enumerate(steps):
    r,c=divmod(i,4); x=24+c*(w+g); y=84+r*(h+50)
    fill,st=(C["green_l"],C["green"]) if i<6 else (C["orange_l"],C["orange"])
    s.rect(x,y,w,h,fill,st); s.text(x+28,y+h/2,str(i+1),18,st,weight=700); s.text(x+w/2+14,y+h/2,t,15,weight=600)
    if c<3: s.arrow(x+w+2,y+h/2,x+w+g-2,y+h/2)
s.path(f"M {24+3*(w+g)+w/2} {84+h+2} C {24+3*(w+g)+w/2} {84+h+30}, {24+w/2} {84+h+20}, {24+w/2} {84+h+48}")
s.save(P("overview-8-processes.svg"))

# 3. 사업 모델
s=S(880,250,"반도체 사업 모델 세 가지")
s.heading("반도체 사업 모델 세 가지")
s.rect(24,70,250,160,C["card"]); s.text(149,92,"종합반도체기업 (IDM)",15,weight=700)
s.box(44,112,210,40,"설계",C["purple_l"],C["purple"]); s.arrow(149,154,149,170); s.box(44,172,210,40,"생산",C["green_l"],C["green"])
s.text(149,222,"예: 메모리사업부",12,C["sub"])
s.rect(300,70,556,160,C["card"]); s.text(578,92,"팹리스 + 파운드리 (분업)",15,weight=700)
s.box(330,120,200,60,"팹리스",C["purple_l"],C["purple"],sub="설계만 담당")
s.box(626,120,200,60,"파운드리",C["green_l"],C["green"],sub="생산만 담당")
s.arrow(532,140,624,140); s.text(578,128,"설계 도면",12,C["sub"])
s.arrow(624,165,532,165); s.text(578,178,"완성된 칩",12,C["sub"])
s.text(430,205,"예: S.LSI사업부(공식 소개 기준)",12,C["sub"]); s.text(726,205,"예: Foundry사업부",12,C["sub"])
s.save(P("overview-business-models.svg"))

# 4. DS부문 조직 지도
s=S(880,330,"DS부문 조직 지도")
s.heading("DS부문 조직 한눈에 보기","이 책 1부에서 다루는 9개 조직을 역할별로 묶었습니다")
groups=[("제품 사업",C["blue_l"],C["blue"],["메모리사업부","S.LSI사업부","Foundry사업부"]),
        ("연구",C["purple_l"],C["purple"],["CTO 반도체연구소","SAIT"]),
        ("제조·후공정",C["green_l"],C["green"],["글로벌 제조&인프라총괄","TSP총괄"]),
        ("AI·신사업",C["orange_l"],C["orange"],["AX/PI센터","CSS사업팀"])]
gw=200;gg=12
for i,(g,f,st,items) in enumerate(groups):
    x=24+i*(gw+gg); s.rect(x,76,gw,236,C["card"],st); s.text(x+gw/2,98,g,15,st,weight=700)
    for j,t in enumerate(items): s.box(x+14,118+j*62,gw-28,48,t,f,st,size=14)
s.save(P("ds-org-map.svg"))

# 5. DRAM vs NAND
s=S(880,330,"DRAM 셀과 3D NAND 구조 비교")
s.heading("DRAM과 NAND는 이렇게 다르게 생겼어요","개념을 단순화한 그림입니다")
s.rect(24,74,404,236,C["card"]); s.text(226,96,"DRAM 셀 (1T1C)",15,weight=700)
s.line(70,140,70,250,C["blue"],3); s.text(82,240,"비트라인",12,C["sub"],"start")
s.line(70,200,140,200,C["ink"]); s.rect(140,180,60,40,C["blue_l"],C["blue"],4); s.text(170,200,"T",14,weight=700)
s.line(170,180,170,140,C["purple"],3); s.line(100,140,380,140,C["purple"],3); s.text(320,126,"워드라인(스위치 켜기)",12,C["sub"])
s.line(200,200,260,200); s.line(260,180,260,220,C["ink"],3); s.line(274,180,274,220,C["ink"],3); s.line(274,200,320,200)
s.text(267,238,"커패시터",12,C["sub"]); s.text(334,200,"⏚",18)
s.text(250,262,"전하가 있으면 1, 없으면 0",13,C["blue"],weight=600)
s.text(226,288,"전하가 새므로 주기적으로 다시 써야 함(Refresh)",12,C["sub"])
s.rect(452,74,404,236,C["card"]); s.text(654,96,"3D NAND (V-NAND)",15,weight=700)
for k in range(6):
    y=128+k*26; s.rect(500,y,240,18,C["green_l"],C["green"],3); s.text(770,y+9,f"셀 층 {6-k}",11,C["sub"],"start")
s.rect(608,116,24,172,C["orange_l"],C["orange"],6); s.text(600,112,"수직 채널 →",12,C["orange"],"end",600)
s.text(654,298+0,"",1)
s.text(560,300,"",1)
s.text(654,298,"층을 위로 쌓아 용량을 늘림",12,C["green"],"middle",600)
s.save(P("memory-dram-nand.svg"))

# 6. HBM
s=S(880,270,"HBM 적층 구조")
s.heading("HBM: DRAM을 쌓고 관통 전극(TSV)으로 연결","개념을 단순화한 단면도")
s.rect(60,226,760,22,C["gray_l"],C["line"],4); s.text(440,237,"패키지 기판",12,C["sub"])
s.rect(90,202,700,22,C["teal_l"],C["teal"],4); s.text(440,213,"인터포저 (칩끼리 연결하는 중간 기판)",12,C["ink"])
for k in range(4):
    y=170-k*26; s.rect(120,y,300,22,C["blue_l"],C["blue"],3); s.text(270,y+11,f"DRAM 칩 {k+1}",12,weight=600)
s.rect(120,196,300,6,C["orange_l"],C["orange"],2)
for xx in (170,230,310,370): s.line(xx,96,xx,202,C["orange"],3)
s.text(440,110,"주황색 선 = TSV",12,C["orange"],"start",600)
s.rect(500,130,260,70,C["purple_l"],C["purple"],6); s.text(630,165,"GPU / AI 가속기",14,weight=700)
s.save(P("memory-hbm.svg"))

# 7. 공통 학습 로드맵
s=S(880,220,"직무별 4단계 학습 로드맵")
s.heading("모든 직무 장의 4단계 학습 로드맵","기간은 학기 중 병행 기준의 대략적인 가이드")
st=[("1단계 입문","1~2개월","큰 그림 잡기",C["blue_l"],C["blue"]),("2단계 기본기","3~4개월","교과서 수준 직접 해보기",C["green_l"],C["green"]),
    ("3단계 심화","3~6개월","한 갈래 끝까지",C["purple_l"],C["purple"]),("4단계 포트폴리오","2~3개월","보여줄 수 있게 정리",C["orange_l"],C["orange"])]
w=190
for i,(a,b,c,f,stc) in enumerate(st):
    x=24+i*(w+18); s.rect(x,80,w,110,f,stc); s.text(x+w/2,106,a,15,weight=700); s.text(x+w/2,134,b,13,stc,weight=600); s.text(x+w/2,162,c,13,C["sub"])
    if i<3: s.arrow(x+w+1,135,x+w+17,135)
s.save(P("roadmap-4steps.svg"))

# 8. 회로설계 흐름
s=S(880,270,"회로설계 업무 흐름")
s.heading("회로설계는 이렇게 진행돼요","문제가 생기면 앞 단계로 돌아가 다시 설계합니다")
st=["사양 정의","회로 설계","시뮬레이션\n(코너 검증)","레이아웃","검증\n(DRC·LVS)","칩 제작·측정"]
w=122;g=20
for i,t in enumerate(st):
    x=24+i*(w+g); s.box(x,90,w,72,t,size=14)
    if i<5: s.arrow(x+w+2,126,x+w+g-2,126)
xa=24+1*(w+g)+w/2; xb=24+2*(w+g)+w/2; xc=24+5*(w+g)+w/2
s.path(f"M {xb} 164 C {xb} 196, {xa+20} 196, {xa+20} 166",C["red"],dash="5 4"); s.text((xa+xb)/2+10,206,"사양 미달 → 수정",12,C["red"])
s.path(f"M {xc} 164 L {xc} 228 L {xa-20} 228 L {xa-20} 166",C["red"],dash="5 4"); s.text((xb+xc)/2+40,248,"측정 결과가 다르면 원인을 찾아 다시 설계",12,C["red"])
s.save(P("circuit-design-flow.svg"))

# 9. 트랜지스터 구조 진화
s=S(880,310,"트랜지스터 구조: Planar, FinFET, GAA")
s.heading("트랜지스터 구조의 변화","게이트가 채널을 감싸는 면이 넓어질수록 전류를 더 잘 제어합니다")
cols=[("Planar","게이트가 위 1면",1),("FinFET","게이트가 3면을 감쌈",3),("GAA","게이트가 4면을 감쌈",4)]
for i,(n,d,k) in enumerate(cols):
    x=24+i*284; s.rect(x,74,260,196,C["card"]); s.text(x+130,96,n,16,weight=700)
    cx=x+130
    s.rect(x+40,214,180,16,C["gray_l"],C["line"],2)
    if k==1:
        s.rect(cx-60,192,120,22,C["green_l"],C["green"],3); s.rect(cx-50,160,100,30,C["purple_l"],C["purple"],4)
    elif k==3:
        s.rect(cx-62,120,124,94,C["purple_l"],C["purple"],6); s.rect(cx-16,134,32,80,C["green_l"],C["green"],3)
    else:
        s.rect(cx-62,116,124,98,C["purple_l"],C["purple"],6)
        for j in range(3): s.rect(cx-40,128+j*28,80,14,C["green_l"],C["green"],3)
    s.text(cx,248,d,13,C["sub"])
s.text(440,290,"보라 = 게이트, 초록 = 채널(전류가 흐르는 길), 회색 = 기판",12,C["sub"])
s.save(P("transistor-structures.svg"))

# 10. 패키지 종류
s=S(880,300,"패키지 종류 비교")
s.heading("패키지는 이렇게 발전했어요","왼쪽에서 오른쪽으로 갈수록 연결이 짧고 촘촘해집니다")
names=["와이어 본딩","플립칩","2.5D (인터포저)","3D 적층"]
for i,n in enumerate(names):
    x=24+i*212; s.rect(x,74,198,206,C["card"]); s.text(x+99,96,n,15,weight=700)
    s.rect(x+20,236,158,16,C["gray_l"],C["line"],3)
    if i==0:
        s.rect(x+60,196,78,30,C["blue_l"],C["blue"],3)
        s.path(f"M {x+64} 198 Q {x+40} 170 {x+34} 236",C["orange"],2,False); s.path(f"M {x+134} 198 Q {x+158} 170 {x+164} 236",C["orange"],2,False)
        s.text(x+99,266,"가는 금속선으로 연결",12,C["sub"])
    elif i==1:
        s.rect(x+50,200,98,28,C["blue_l"],C["blue"],3)
        for b in range(5): s.add(f'<circle cx="{x+60+b*20}" cy="{232}" r="4" fill="{C["orange"]}"/>')
        s.text(x+99,266,"칩을 뒤집어 범프로 연결",12,C["sub"])
    elif i==2:
        s.rect(x+30,216,138,16,C["teal_l"],C["teal"],3); s.rect(x+38,188,54,26,C["blue_l"],C["blue"],3); s.rect(x+104,180,56,34,C["purple_l"],C["purple"],3)
        s.text(x+99,266,"칩 여러 개를 나란히",12,C["sub"])
    else:
        for k in range(4): s.rect(x+60,204-k*28,78,24,C["blue_l"],C["blue"],3)
        for xx in (x+80,x+118): s.line(xx,124,xx,234,C["orange"],3)
        s.text(x+99,266,"칩을 쌓고 TSV로 관통 연결",12,C["sub"])
s.save(P("package-types.svg"))

# 11. 단위 공정 반복
s=S(880,300,"단위 공정이 반복되는 구조")
s.heading("단위 공정은 한 번이 아니라 수십~수백 번 반복돼요","한 층을 만들 때마다 아래 순환을 거칩니다")
cx,cy,R=330,190,82
pts=[("증착",cx,cy-R),("포토(노광)",cx+R*1.6,cy),("식각",cx,cy+R),("세정·검사",cx-R*1.6,cy)]
for t,x,y in pts: s.box(x-62,y-22,124,44,t,C["green_l"],C["green"],size=14)
s.path(f"M {cx+64} {cy-R} Q {cx+R*1.6} {cy-R} {cx+R*1.6} {cy-24}")
s.path(f"M {cx+R*1.6} {cy+24} Q {cx+R*1.6} {cy+R} {cx+64} {cy+R}")
s.path(f"M {cx-64} {cy+R} Q {cx-R*1.6} {cy+R} {cx-R*1.6} {cy+24}")
s.path(f"M {cx-R*1.6} {cy-24} Q {cx-R*1.6} {cy-R} {cx-64} {cy-R}")
s.text(cx,cy,"한 층",15,C["green"],weight=700)
s.rect(600,110,256,160,C["card"]); s.text(728,132,"공정기술 엔지니어의 관점",14,weight=700)
for j,t in enumerate(["목표: 두께·모양·위치를 정확하게","안정: 매번 같은 결과(SPC)","속도: 더 빨리, 더 많이(생산성)"]):
    s.text(616,164+j*30,"• "+t,13,C["sub"],"start")
s.save(P("process-cycle.svg"))

# 12. 원인 분석 고리
s=S(880,240,"불량 원인 분석 과정")
s.heading("평가 및 분석: 원인을 좁혀 가는 과정")
st=["현상 발견","가설 세우기","데이터·실험","검증","원인 확정·개선"]
w=146;g=24
for i,t in enumerate(st):
    x=24+i*(w+g); f,stc=(C["orange_l"],C["orange"]) if i==4 else (C["blue_l"],C["blue"])
    s.box(x,84,w,60,t,f,stc,size=14)
    if i<4: s.arrow(x+w+2,114,x+w+g-2,114)
x3=24+3*(w+g)+w/2; x1=24+1*(w+g)+w/2
s.path(f"M {x3} 146 C {x3} 206, {x1} 206, {x1} 148",C["red"],dash="5 4"); s.text((x1+x3)/2,214,"가설이 틀리면 다음 가설로",12,C["red"])
s.save(P("analysis-loop.svg"))

# 13. 공급망
s=S(880,300,"반도체 공급망과 사업 직무")
s.heading("반도체 공급망과 사업·지원 직무가 일하는 지점")
st=[("소재·장비\n협력사",C["gray_l"],C["line"]),("웨이퍼 제조\n(팹)",C["green_l"],C["green"]),("조립·테스트\n(TSP·OSAT)",C["orange_l"],C["orange"]),("고객사",C["purple_l"],C["purple"])]
w=170;g=48
for i,(t,f,stc) in enumerate(st):
    x=24+i*(w+g); s.box(x,90,w,70,t,f,stc,size=14)
    if i<3: s.arrow(x+w+2,125,x+w+g-2,125)
roles=[(0,0,"구매",C["blue"]),(1,2,"생산관리: 계획·일정·재고",C["teal"]),(3,3,"영업마케팅",C["purple"])]
for a,b,t,col in roles:
    xa=24+a*(w+g); xb=24+b*(w+g)+w
    s.rect(xa,184,xb-xa,36,"#ffffff",col,8,2); s.text((xa+xb)/2,202,t,13,col,weight=700)
s.rect(24,236,4*w+3*g,40,C["card"],C["line"],8); s.text(24+(4*w+3*g)/2,256,"경영지원(재무·일반)·인사: 전체 흐름의 돈·계획·사람을 지원",13,C["sub"],weight=600)
s.save(P("supply-chain.svg"))

# 14. 팹 건물 단면
s=S(880,320,"반도체 공장 건물 단면")
s.heading("반도체 공장(팹) 건물은 층마다 역할이 달라요","개념을 단순화한 단면도")
s.rect(60,80,560,40,C["gray_l"],C["line"],4); s.text(340,100,"공조 설비층: 필터를 거친 깨끗한 공기를 아래로 불어 줌",13,weight=600)
s.rect(60,124,560,70,C["blue_l"],C["blue"],4); s.text(340,159,"클린룸: 장비와 웨이퍼가 있는 생산 공간",14,weight=700)
for xx in (90,130,550,590): s.arrow(xx,126,xx,186,C["blue"],1.5)
s.rect(60,198,560,70,C["teal_l"],C["teal"],4); s.text(340,233,"하부 유틸리티층: 배관·전력·배기·펌프",14,weight=700)
s.rect(60,272,560,30,C["gray_l"],C["line"],4); s.text(340,287,"기초·진동 관리 구조",12,C["sub"])
s.rect(650,80,206,222,C["card"]); s.text(753,102,"공장으로 공급되는 것",14,weight=700)
for j,t in enumerate(["전력 (수변전)","초순수 (UPW)","특수·벌크 가스","화학 약품","냉각수·압축 공기"]):
    s.text(670,134+j*32,"• "+t,13,C["sub"],"start")
s.save(P("fab-layers.svg"))

# 15. 신호 및 시스템 설계 흐름
s=S(880,230,"알고리즘에서 칩까지")
s.heading("신호 및 시스템 설계: 알고리즘이 칩이 되기까지")
st=[("알고리즘 연구","수식·논문"),("부동소수점 모델","Python/MATLAB"),("고정소수점 변환","비트 수 결정"),("하드웨어 구조","연산기·메모리"),("RTL 구현","회로설계와 협업")]
w=148;g=22
for i,(a,b) in enumerate(st):
    x=24+i*(w+g); s.box(x,84,w,70,a,C["purple_l"],C["purple"],size=14,sub=b)
    if i<4: s.arrow(x+w+2,119,x+w+g-2,119)
s.text(440,190,"각 단계에서 성능 손실과 연산량(하드웨어 비용)을 함께 확인합니다",13,C["sub"])
s.save(P("signal-system-flow.svg"))

# 16. CAE 고리
s=S(880,240,"CAE 시뮬레이션 작업 흐름")
s.heading("CAE시뮬레이션: 예측하고, 실측과 비교하고, 보정하기")
st=[("물리 모델","방정식·격자"),("시뮬레이션","대량 실행"),("실측과 비교","오차 확인"),("모델 보정","변수 조정"),("빠른 예측 모델","AI 대리 모델")]
w=148;g=22
for i,(a,b) in enumerate(st):
    x=24+i*(w+g); f,stc=(C["orange_l"],C["orange"]) if i==4 else (C["green_l"],C["green"])
    s.box(x,84,w,70,a,f,stc,size=14,sub=b)
    if i<4: s.arrow(x+w+2,119,x+w+g-2,119)
x3=24+3*(w+g)+w/2; x1=24+1*(w+g)+w/2
s.path(f"M {x3} 156 C {x3} 212, {x1} 212, {x1} 158",C["red"],dash="5 4"); s.text((x1+x3)/2,220,"오차가 크면 다시 시뮬레이션",12,C["red"])
s.save(P("cae-loop.svg"))

# 17. 채용 흐름
s=S(880,220,"일반적인 신입 채용 흐름")
s.heading("일반적인 신입 채용 흐름","직무와 연도에 따라 달라질 수 있으니 공고를 꼭 확인하세요")
st=[("지원서·에세이","역량과 경험 연결"),("직무적합성 평가","전공·경험 검토"),("GSAT","수리·추리\n(S/W는 별도 테스트)"),("면접","직무·인성 등"),("건강검진","최종 단계")]
w=148;g=22
for i,(a,b) in enumerate(st):
    x=24+i*(w+g); s.box(x,84,w,86,a,C["blue_l"],C["blue"],size=14)
    s.text(x+w/2,186,b,12,C["sub"])
    if i<4: s.arrow(x+w+2,127,x+w+g-2,127)
s.save(P("recruiting-flow.svg"))
print("done")
