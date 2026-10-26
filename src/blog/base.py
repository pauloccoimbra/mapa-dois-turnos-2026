import json, html
from charts import *
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
S=json.load(open(ROOT/'dados/derivados/estudos_stats.json'))
A=S['acc']; T=S['T']
PAGE='https://pauloccoimbra.github.io/mapa-dois-turnos-2026/'; REPO='https://github.com/pauloccoimbra/mapa-dois-turnos-2026'
def M(x,dec=2): return nb(x/1e6,dec)+' milhões'
def Mn(x,dec=2): return nb(x/1e6,dec)
def P(x,dec=1): return nb(x,dec)+'%'
def pp(x,dec=1,sign=True): return nb(x,dec,sign)+' p.p.'
def N(x): return nb(x,0)
def tc(s):
    out=[];  
    for i,w in enumerate(s.lower().split(' ')):
        out.append(w if (i>0 and w in ('de','da','do','das','dos','e')) else w[:1].upper()+w[1:])
    return ' '.join(out)
REGNAME={'Norte':'Norte','Nordeste':'Nordeste','Sudeste':'Sudeste','Sul':'Sul','Centro-Oeste':'Centro-Oeste','Exterior':'Exterior'}
FS='font-size:15px;line-height:1.65;color:#15202b'
def h2(t): return f'<h2 style="font-size:20px;line-height:1.3;margin:28px 0 8px">{t}</h2>'
def p(t): return f'<p style="margin:0 0 14px">{t}</p>'
def fig(svg,cap): return f'<figure style="margin:18px 0;padding:0">{svg}<figcaption style="font-size:13px;color:#5b6978;margin-top:6px;text-align:left">{cap}</figcaption></figure>'
def table(head,rows,al=None,cap=None,small=False):
    al=al or ['left']+['right']*(len(head)-1); fs='13px' if small else '14px'
    h=''.join(f'<th style="text-align:{a};padding:6px 8px;border-bottom:2px solid #15202b;font-weight:700;white-space:nowrap">{c}</th>' for c,a in zip(head,al))
    b=''
    for r in rows:
        b+='<tr>'+''.join(f'<td style="text-align:{a};padding:5px 8px;border-bottom:1px solid #e3e7eb;white-space:nowrap">{c}</td>' for c,a in zip(r,al))+'</tr>'
    c=f'<div style="font-size:13px;color:#5b6978;margin:0 0 4px;text-align:left">{cap}</div>' if cap else ''
    return f'<div style="margin:16px 0">{c}<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:{fs};font-variant-numeric:tabular-nums"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div></div>'
def box(t): return f'<div style="border-left:4px solid #0e7c86;background:#f4f7f9;padding:10px 14px;margin:18px 0;font-size:14px;line-height:1.6">{t}</div>'
FOOT=(f'<hr style="border:0;border-top:1px solid #e3e7eb;margin:28px 0 12px">'
      f'<p style="font-size:13px;color:#5b6978;line-height:1.55;margin:0 0 8px">Dados: arquivos públicos de divulgação do TSE (totalização por município e zona), 1º e 2º turnos de 2026, lidos em 26/10/2026; '
      f'os números podem diferir dos resultados finais oficiais se os arquivos forem atualizados. Mapa interativo: <a href="{PAGE}">{PAGE}</a>. '
      f'Código, dados e metodologia: <a href="{REPO}">{REPO}</a>. Este texto é descritivo e não partidário: usa apenas totais oficiais agregados por zona eleitoral, sem dados pessoais.</p>')
def post(inner,serie=''): 
    return f'<div style="{FS}">{inner}{FOOT}</div>'.replace('p.p..','p.p.')
POSTS=[]
def reg(num,slug,title,desc,labels,fn): POSTS.append(dict(num=num,slug=slug,title=title,desc=desc,labels=labels,fn=fn))
