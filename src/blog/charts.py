"""Gráficos SVG autocontidos (fundo branco, fontes do sistema) para os posts."""
import html
INK='#15202b'; MUT='#5b6978'; GRID='#e3e7eb'; LULA='#0e7c86'; FLA='#c9780a'; BLU='#3a66b5'; GRY='#98a3ae'; LGR='#d5dbe1'
FONT='font-family="Arial,Helvetica,sans-serif"'
def nb(x,dec=1,sign=False):
    s=f'{abs(x):,.{dec}f}'.replace(',','X').replace('.',',').replace('X','.')
    if x<0 and float(f'{abs(x):.{dec}f}')!=0: return '−'+s
    return ('+' if sign and float(f'{abs(x):.{dec}f}')!=0 else '')+s
def esc(s): return html.escape(str(s),quote=True)
class Svg:
    def __init__(s,w,h,title,desc=''):
        s.w,s.h=w,h; s.p=[]; s.title=title; s.desc=desc
    def add(s,x): s.p.append(x)
    def text(s,x,y,t,size=12.5,anchor='start',fill=INK,weight='400',**kw):
        s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{esc(t)}</text>')
    def line(s,x1,y1,x2,y2,c=GRID,w=1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>')
    def rect(s,x,y,w,h,fill,rx=0):
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" fill="{fill}" rx="{rx}"/>')
    def circ(s,x,y,r,fill,stroke='#fff',sw=1.5):
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def out(s):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="100%" role="img" aria-label="{esc(s.title)}" '
                f'style="max-width:{s.w}px;height:auto;display:block;margin:0 auto;background:#fff" {FONT}><title>{esc(s.title)}</title>'
                f'<rect width="{s.w}" height="{s.h}" fill="#fff"/>'+''.join(s.p)+'</svg>')
def scale(d0,d1,r0,r1): return lambda v: r0+(v-d0)/(d1-d0)*(r1-r0)
def ticks(sv,x0,x1,top,bot,vals,fmt=lambda v:nb(v,0),unit=''):
    for v in vals:
        sv.line(sv(v) if False else x0(v),top,x0(v),bot,GRID)
        sv.text(x0(v),bot+14,fmt(v),11.5,'middle',MUT)
def dumbbell(rows,title,xlim,xticks,xlabel,w=520,rowh=21,left=150,right=22,lab1='1º turno',lab2='2º turno',zero=True,fmt=lambda v:nb(v,1,True),sortnote=None,highlight=()):
    """rows: (rótulo, v1, v2). Seta do 1º ao 2º turno; cor pelo lado do 2º turno (Lula<0, Flávio>0)."""
    top=34; n=len(rows); h=top+n*rowh+44
    sv=Svg(w,h,title); X=scale(xlim[0],xlim[1],left,w-right)
    for v in xticks:
        sv.line(X(v),top-6,X(v),h-40,GRID if v!=0 else '#9aa5b0',1 if v!=0 else 1.4); sv.text(X(v),h-24,nb(v,0,True) if v else '0',11.5,'middle',MUT)
    sv.text(w-right,h-6,xlabel,11.5,'end',MUT)
    # legenda
    sv.circ(left+4,12,4.5,'#fff',GRY,1.8); sv.text(left+13,16,lab1,12,fill=MUT); sv.circ(left+80,12,4.5,LULA); sv.text(left+89,16,lab2+' (Lula à frente)',12,fill=MUT)
    sv.circ(left+232,12,4.5,FLA); sv.text(left+241,16,'(Flávio à frente)',12,fill=MUT)
    for i,(lab,a,b) in enumerate(rows):
        y=top+i*rowh+rowh/2; col=LULA if b<0 else FLA
        bold='700' if lab in highlight else '400'
        sv.text(left-8,y+4,lab,12.5,'end',INK,bold)
        sv.line(X(a),y,X(b),y,'#b7c0c9',2.2); sv.circ(X(a),y,4.5,'#fff',GRY,1.8); sv.circ(X(b),y,5.2,col)
    return sv.out()
def hbars(rows,title,xmax,xticks,xlabel,w=520,rowh=24,left=150,right=70,fmt=lambda v:nb(v,1),colors=None,ref=None,reflab=''):
    top=26; n=len(rows); h=top+n*rowh+38
    sv=Svg(w,h,title); X=scale(0,xmax,left,w-right)
    for v in xticks: sv.line(X(v),top-6,X(v),h-36,GRID); sv.text(X(v),h-20,nb(v,0),11.5,'middle',MUT)
    sv.text(left+(w-right-left)/2,h-1,xlabel,11.5,'middle',MUT)
    for i,r in enumerate(rows):
        lab,v=r[0],r[1]; c=(colors[i] if colors else LULA); y=top+i*rowh
        sv.text(left-8,y+rowh/2+4,lab,12.5,'end'); sv.rect(left,y+4,X(v)-left,rowh-9,c,2); sv.text(X(v)-5,y+rowh/2+4,fmt(v),12,'end','#fff','700')
    if ref is not None:
        sv.line(X(ref),top-6,X(ref),h-36,INK,1.3,'4 3'); sv.text(X(ref),top-10,reflab,11.5,'middle',INK)
    return sv.out()
def stackbar(parts,title,total_lab,w=520,height=30):
    """Uma barra empilhada horizontal com legenda em linhas. parts: (rótulo, valor, cor, texto)"""
    tot=sum(p[1] for p in parts); left=12; right=12; X=(w-left-right)/tot; n=len(parts)
    sv=Svg(w,26+height+14+n*20,title); x=left; sv.text(left,16,total_lab,12.5,'start',INK,'700')
    for i,(lab,v,c,tx) in enumerate(parts):
        sv.rect(x+(1 if i else 0),26,v*X-(2 if i else 0),height,c); x+=v*X
        y=26+height+22+i*20; sv.rect(left,y-10,11,11,c,2); sv.text(left+18,y,lab,12.5,'start',INK); sv.text(w-right,y,tx,12.5,'end',MUT)
    return sv.out()
def stack100(rows,cols,title,w=520,rowh=30,left=142,right=14,legend=True):
    """rows: (rótulo, [pcts...]); cols: (rótulo,cor). Barras 100%."""
    top=34 if legend else 10; n=len(rows); h=top+n*rowh+8
    sv=Svg(w,h,title); X=scale(0,100,left,w-right)
    if legend:
        x=left
        for lab,c in cols: sv.rect(x,8,11,11,c,2); sv.text(x+16,18,lab,11.5,fill=MUT); x+=16+len(lab)*6.3+14
    for i,(lab,vals) in enumerate(rows):
        y=top+i*rowh; sv.text(left-8,y+rowh/2+3,lab,12.5,'end'); x=0
        for (cl,c),v in zip(cols,vals):
            if v<=0: continue
            sv.rect(X(x)+0.7,y+3,X(x+v)-X(x)-1.4,rowh-8,c)
            if v>=7: sv.text((X(x)+X(x+v))/2,y+rowh/2+3,nb(v,1 if v>=95 else 0)+'%' if (v>=10 or v<0.5) else nb(v,1)+'%',11.5,'middle','#fff' if c in (LULA,BLU,FLA) else INK,'700')
            x+=v
    return sv.out()
def vbars(vals,labels,title,ylab,w=520,h=250,ymin=0,ymax=100,colors=None,fmt=lambda v:nb(v,0)+'%',xlabel='',left=46,yticks=None):
    bot=h-44; top=22; n=len(vals); sv=Svg(w,h,title); Y=scale(ymin,ymax,bot,top); bw=(w-left-14)/n
    for v in (yticks or [ymin,(ymin+ymax)/2,ymax]):
        sv.line(left,Y(v),w-8,Y(v),GRID if v!=0 else '#9aa5b0'); sv.text(left-6,Y(v)+4,nb(v,0),11.5,'end',MUT)
    sv.text(left,11,ylab,11.5,'start',MUT)
    for i,(v,lab) in enumerate(zip(vals,labels)):
        x=left+i*bw+bw*0.16; c=colors[i] if colors else LULA
        y0,y1=sorted([Y(0 if ymin<=0<=ymax else ymin),Y(v)]); sv.rect(x,y0,bw*0.68,y1-y0,c,2)
        inside=(v>=ymax*0.9); sv.text(x+bw*0.34,(Y(v)+15) if inside else ((Y(v)-6) if v>=0 else (Y(v)+14)),fmt(v),12,'middle','#fff' if inside else INK,'700' if inside else '400')
        sv.text(x+bw*0.34,bot+16,lab,11.5,'middle',INK)
    if xlabel: sv.text(left+(w-left)/2,h-6,xlabel,11.5,'middle',MUT)
    return sv.out()
def hist(edges,shares,title,w=520,h=240,xlabel='',hi=None,left=40):
    bot=h-44; top=22; sv=Svg(w,h,title); n=len(shares); ymax=max(shares)*1.12; Y=scale(0,ymax,bot,top); X=scale(edges[0],edges[-1],left,w-12)
    for v in [0,ymax/2,ymax]: pass
    for t in range(int(edges[0]),int(edges[-1])+1,2): sv.line(X(t),top,X(t),bot,GRID if t!=0 else '#9aa5b0'); sv.text(X(t),bot+15,nb(t,0),11.5,'middle',MUT)
    sv.line(left,bot,w-12,bot,'#9aa5b0')
    for i,s in enumerate(shares):
        c=LULA if edges[i+1]<=0 else FLA
        sv.rect(X(edges[i])+1,Y(s),X(edges[i+1])-X(edges[i])-2,bot-Y(s),c,1)
    sv.text(left-6,top-8,'% dos votos válidos',11.5,'start',MUT); sv.text((left+w)/2,h-6,xlabel,11.5,'middle',MUT)
    return sv.out()
def strip(cities,title,xlim=(-60,40),xticks=(-60,-40,-20,0,20,40),w=520,rowh=34,left=118,right=18):
    """cities: (rótulo, [(m2,eleitorado),...], m2_cidade). Um ponto por zona; losango = município."""
    top=26; n=len(cities); h=top+n*rowh+44; sv=Svg(w,h,title); X=scale(xlim[0],xlim[1],left,w-right)
    for v in xticks: sv.line(X(v),top-8,X(v),h-40,GRID if v else '#9aa5b0',1 if v else 1.4); sv.text(X(v),h-24,nb(v,0,True) if v else '0',11.5,'middle',MUT)
    sv.text(w-right,h-6,'margem no 2º turno, p.p. (− Lula à frente, + Flávio à frente)',11.5,'end',MUT)
    for i,(lab,pts,mc) in enumerate(cities):
        y=top+i*rowh+rowh/2; sv.text(left-8,y+4,lab,12.5,'end'); sv.line(left,y,w-right,y,'#f0f2f4')
        for m,e in sorted(pts,key=lambda t:-t[1]):
            sv.circ(X(m),y,2.6+min(e,250000)/250000*3.2,LULA if m<0 else FLA,'#fff',1)
        xm=X(mc); sv.add(f'<path d="M{xm:.1f} {y-9:.1f} L{xm+5.5:.1f} {y:.1f} L{xm:.1f} {y+9:.1f} L{xm-5.5:.1f} {y:.1f}Z" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    return sv.out()
