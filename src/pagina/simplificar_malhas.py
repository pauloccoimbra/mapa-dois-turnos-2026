"""Simplifica as malhas municipais (topologia preservada), quantiza e codifica por deltas.
Uso: python3 src/pagina/simplificar_malhas.py 0.008 250  (após baixar_malhas.py)   (TOL em graus, Q = passos por grau). Audita a área de cada município
contra a malha de origem e usa um plano B quando a simplificação distorce o polígono."""
import json,sys,shapely,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
ORI=ROOT/"dados"/"geo"/"origem"
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely import make_valid
TOL=float(sys.argv[1]); Q=float(sys.argv[2])
UFS=[11,12,13,14,15,16,17,21,22,23,24,25,26,27,28,29,31,32,33,35,41,42,43,50,51,52,53]
def polys(g):
    return [g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.geom_type=='Polygon']
def quant(g):
    """polígonos quantizados (grade 1/Q grau) a partir de geometria shapely; descarta anéis degenerados"""
    out=[]
    for p in polys(g):
        rs=[]
        for ring in [p.exterior]+list(p.interiors):
            q=[]
            for x,y in ring.coords:
                pt=(round(x*Q),round(y*Q))
                if not q or pt!=q[-1]: q.append(pt)
            if len(q)>=4: rs.append(q)
        if rs: out.append(rs)
    return out
def area_q(polys_q):
    a=0
    for rs in polys_q:
        for k,r in enumerate(rs):
            s=0
            for (x0,y0),(x1,y1) in zip(r,r[1:]): s+=x0*y1-x1*y0
            a+= (abs(s)/2)*(1 if k==0 else -1)
    return a/(Q*Q)
def enc(polys_q):
    rings=[]; nv=0
    for rs in polys_q:
        for r in rs:
            px=py=0; s=[]
            for x,y in r[:-1]:
                s.append(f'{x-px},{y-py}'); px,py=x,y
            nv+=len(s); rings.append(' '.join(s))
    return '|'.join(rings),nv
out={}; nv=0; fallback=[]; worst=[]
for c in UFS:
    j=json.load(open(ORI/f'g{c}.json'))
    ids=[int(f['properties']['id']) for f in j['features']]
    geoms=[]
    for f in j['features']:
        g=shape(f['geometry'])
        geoms.append(g if g.is_valid else make_valid(g))
    try: cs=list(shapely.coverage_simplify(geoms,TOL))
    except Exception as e: cs=[None]*len(geoms)
    items=[]
    for i,g0,g in zip(ids,geoms,cs):
        a0=g0.area; ok=False
        for how in ('cov','topo','raw'):
            if how=='cov': cand=g
            elif how=='topo': cand=g0.simplify(TOL,preserve_topology=True)
            else: cand=g0
            if cand is None or cand.is_empty: continue
            pq=quant(cand)
            if not pq: continue
            r=area_q(pq)/a0 if a0>0 else 1
            if abs(r-1)<=0.12 or how=='raw':
                ok=True; break
        if how!='cov': fallback.append((i,how,round(r,3)))
        worst.append((abs(r-1),i,how))
        e,n=enc(pq); nv+=n; items.append([i,e])
    out[str(c)]=items
worst.sort(reverse=True)
s=json.dumps(out,separators=(',',':'))
print(TOL,Q,round(len(s)/1e6,2),'MB',nv,'vértices;',len(fallback),'municípios com plano B; pior desvio de área:',[(round(a,3),i,h) for a,i,h in worst[:5]])
json.dump(out,open(ROOT/'dados'/'geo'/'malha_municipal_simplificada.json','w'),separators=(',',':'))
