"""Estudos derivados da base por zona (dados/zonas_2026_t1_t2.csv). Gera stats.json com todos os números citados nos posts."""
import sys, json, warnings, pathlib
warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'src'/'analise'))
from lib import load
d = load()
d['F1']=d.r1_c22; d['L1']=d.r1_c13; d['F2']=d.r2_c22; d['L2']=d.r2_c13
d['O1']=d.r1_validos-d.F1-d.L1
d['BN1']=d.r1_brancos+d.r1_nulos; d['BN2']=d.r2_brancos+d.r2_nulos
d['swing']=(d.L2-d.F2)-(d.L1-d.F1)
d['lead1']=np.sign(d.F1-d.L1); d['lead2']=np.sign(d.F2-d.L2)
S={}
def tot(g): return g[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()
def marg(r):
    r['m1']=(r.F1-r.L1)/r.r1_validos*100; r['m2']=(r.F2-r.L2)/r.r2_validos*100; r['dm']=r.m2-r.m1
    r['t1']=r.r1_comp/r.r1_eleitorado*100; r['t2']=r.r2_comp/r.r2_eleitorado*100
    r['bn1']=r.BN1/r.r1_comp*100; r['bn2']=r.BN2/r.r2_comp*100
    r['lead1']=np.sign(r.F1-r.L1); r['lead2']=np.sign(r.F2-r.L2)
    return r
# ---- nacional
T=tot(d); S['T']={k:float(v) for k,v in T.items()}
nf=T.F2+T.L2-T.F1-T.L1
S['acc']=dict(novos=float(nf),outros=float(T.O1),dBN=float(T.BN1-T.BN2),dComp=float(T.r2_comp-T.r1_comp),dL=float(T.L2-T.L1),dF=float(T.F2-T.F1),
  shareL=float((T.L2-T.L1)/nf),swing=float(T.swing),net1=float(T.F1-T.L1),net2=float(T.L2-T.F2),
  m1=float((T.F1-T.L1)/T.r1_validos*100),m2=float((T.F2-T.L2)/T.r2_validos*100),
  L1p=float(T.L1/T.r1_validos*100),F1p=float(T.F1/T.r1_validos*100),O1p=float(T.O1/T.r1_validos*100),L2p=float(T.L2/T.r2_validos*100),F2p=float(T.F2/T.r2_validos*100),
  t1=float(T.r1_comp/T.r1_eleitorado*100),t2=float(T.r2_comp/T.r2_eleitorado*100),bn1=float(T.BN1/T.r1_comp*100),bn2=float(T.BN2/T.r2_comp*100),
  br1=float(d.r1_brancos.sum()/T.r1_comp*100),br2=float(d.r2_brancos.sum()/T.r2_comp*100),nu1=float(d.r1_nulos.sum()/T.r1_comp*100),nu2=float(d.r2_nulos.sum()/T.r2_comp*100))
S['acc']['dm']=S['acc']['m2']-S['acc']['m1']
# ---- regiões e UFs (UF sem exterior)
reg=marg(d.groupby('regiao')[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum())
reg['shareSwing']=reg.swing/T.swing; reg['shareL']=(reg.L2-reg.L1)/((reg.L2-reg.L1)+(reg.F2-reg.F1)); reg['dL']=reg.L2-reg.L1; reg['dF']=reg.F2-reg.F1
reg['elShare']=reg.r1_eleitorado/T.r1_eleitorado
S['reg']=reg.round(4).to_dict('index')
uf=marg(d.groupby('UF')[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()).drop('ZZ')
uf['shareSwing']=uf.swing/T.swing
S['uf']=uf.round(4).to_dict('index')
S['uf_flip']=[k for k in uf.index if uf.loc[k,'lead1']!=uf.loc[k,'lead2']]
S['uf_L1']=int((uf.lead1<0).sum()); S['uf_L2']=int((uf.lead2<0).sum())
S['uf_L2_list']=sorted(uf[uf.lead2<0].index)
# ---- municípios (sem exterior)
mu=marg(d[d.uf!='zz'].groupby(['uf','cod_mun'])[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum())
mu['nome']=d[d.uf!='zz'].groupby(['uf','cod_mun']).municipio.first()
FL=mu[(mu.lead1>0)&(mu.lead2<0)]; LF=mu[(mu.lead1<0)&(mu.lead2>0)]
S['mun']=dict(n=len(mu),FL=len(FL),LF=len(LF),L1=int((mu.lead1<0).sum()),L2=int((mu.lead2<0).sum()),F1=int((mu.lead1>0).sum()),F2=int((mu.lead2>0).sum()),
  FL_elect=float(FL.r1_eleitorado.sum()),FL_mg=int((FL.index.get_level_values(0)=='mg').sum()),FL_sp=int((FL.index.get_level_values(0)=='sp').sum()),
  FL_by_uf=FL.reset_index().groupby('uf').size().sort_values(ascending=False).head(6).to_dict(),
  FL_big=[(r.nome,i[0],float(r.r1_eleitorado),float(r.m1),float(r.m2)) for i,r in FL.sort_values('r1_eleitorado',ascending=False).head(6).iterrows()],
  FL_pct_elect=float(FL.r1_eleitorado.sum()/T.r1_eleitorado*100))
# ---- zonas
z=marg(d[d.uf!='zz'].copy()); z['w']=z.r2_validos; z['mun']=z.uf+'_'+z.cod_mun.astype(str)
FLz=z[(z.lead1>0)&(z.lead2<0)]; LFz=z[(z.lead1<0)&(z.lead2>0)]
def wq(x,w,q):
    i=np.argsort(x.values);x=x.values[i];w=w.values[i];c=np.cumsum(w)/w.sum();c=c-w[np.argsort(np.argsort(i))][i]/w.sum()/2 if False else c;return [float(np.interp(qq,c,x)) for qq in q]
S['z']=dict(n=len(z),FL=len(FLz),LF=len(LFz),L1=int((z.lead1<0).sum()),L2=int((z.lead2<0).sum()),toL=float((z.dm<0).mean()*100),toL_w=float(z.w[z.dm<0].sum()/z.w.sum()*100),
  dm_q=wq(z.dm,z.w,[.05,.25,.5,.75,.95]),tUp=float((z.t2>z.t1).mean()*100),FL_by_uf=FLz.groupby('uf').size().sort_values(ascending=False).head(6).to_dict(),
  swing_neg=int((z.swing<0).sum()))
zs=z.sort_values('swing',ascending=False); cs=zs.swing.cumsum()/zs.swing.sum(); S['z']['half_swing_zones']=int((cs<0.5).sum()+1)
# viés de bins de m1
bins=[(0,2),(2,4),(4,6),(6,8),(8,10),(10,15),(15,200)]
S['flipbin']=[]
for lo,hi in bins:
    c=z[(z.m1>lo)&(z.m1<=hi)]; S['flipbin'].append(dict(lo=lo,hi=hi,n=len(c),share=float((c.lead2<0).mean()*100),dm=float(np.average(c.dm,weights=c.w))))
# histograma de dm ponderado por votos válidos (faixas de 1 p.p.)
edges=np.arange(-14,5,1.0); h,_=np.histogram(z.dm.clip(-13.999,4.999),bins=edges,weights=z.w); S['dmhist']=dict(edges=edges.tolist(),share=(h/h.sum()*100).tolist())
# modelo de deslocamento uniforme
sh=S['acc']['dm']
def rm(p): e=p-z.m2; return float(np.sqrt(np.average(e**2,weights=z.w))),float(np.average(np.abs(e),weights=z.w))
models={'nenhuma mudança':z.m1,'deslocamento nacional único':z.m1+sh}
for nome,key in [('deslocamento por região','regiao'),('deslocamento por UF','uf'),('deslocamento por município','mun')]:
    s_=z.groupby(key).apply(lambda g: np.average(g.dm,weights=g.w)); models[nome]=z.m1+z[key].map(s_)
S['uniforme']=[]
for nome,p in models.items():
    fp=((z.m1>0)&(p<0)); S['uniforme'].append(dict(modelo=nome,rmse=rm(p)[0],mae=rm(p)[1],flips=int(fp.sum()),hit=int((fp&(z.m2<0)).sum()),sign=float(np.average(np.sign(p)==np.sign(z.m2),weights=z.w)*100)))
S['sd_m2']=float(np.sqrt(np.average((z.m2-np.average(z.m2,weights=z.w))**2,weights=z.w)))
unif_uf_flip=[k for k in uf.index if np.sign(uf.loc[k,'m1']+sh)!=np.sign(uf.loc[k,'m1'])]; S['uniforme_uf_flip']=unif_uf_flip
# ---- tamanho
bins_=[0,5e3,10e3,20e3,50e3,100e3,200e3,500e3,1e9]; lab=['até 5 mil','5 a 10 mil','10 a 20 mil','20 a 50 mil','50 a 100 mil','100 a 200 mil','200 a 500 mil','mais de 500 mil']
mu['cl']=pd.cut(mu.r1_eleitorado,bins_,labels=lab)
g=marg(mu.groupby('cl',observed=True)[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()); g['n']=mu.groupby('cl',observed=True).size()
g['shareSwing']=g.swing/T.swing; g['shareL']=(g.L2-g.L1)/((g.L2-g.L1)+(g.F2-g.F1)); g['elShare']=g.r1_eleitorado/T.r1_eleitorado
g['nFL']=mu[(mu.lead1>0)&(mu.lead2<0)].groupby('cl',observed=True).size().reindex(g.index).fillna(0)
S['size']=g.round(4).reset_index().to_dict('records')
caps={'ac':'RIO BRANCO','al':'MACEIÓ','ap':'MACAPÁ','am':'MANAUS','ba':'SALVADOR','ce':'FORTALEZA','df':'BRASÍLIA','es':'VITÓRIA','go':'GOIÂNIA','ma':'SÃO LUÍS','mt':'CUIABÁ','ms':'CAMPO GRANDE','mg':'BELO HORIZONTE','pa':'BELÉM','pb':'JOÃO PESSOA','pr':'CURITIBA','pe':'RECIFE','pi':'TERESINA','rj':'RIO DE JANEIRO','rn':'NATAL','rs':'PORTO ALEGRE','ro':'PORTO VELHO','rr':'BOA VISTA','sc':'FLORIANÓPOLIS','se':'ARACAJU','sp':'SÃO PAULO','to':'PALMAS'}
mu['cap']=[caps.get(i[0])==r.nome.upper() for i,r in mu.iterrows()]
cp=mu[mu.cap]; ot=mu[~mu.cap]; assert len(cp)==27
def agg2(x): 
    r=marg(pd.DataFrame([x[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()])).iloc[0]; return {k:float(v) for k,v in r.items()}
S['cap']=dict(cap=agg2(cp),res=agg2(ot),n=len(cp),elShare=float(cp.r1_eleitorado.sum()/T.r1_eleitorado*100),swShare=float(cp.swing.sum()/T.swing*100),
  tab=[(r.nome,i[0],float(r.r1_eleitorado),float(r.m1),float(r.m2),float(r.dm)) for i,r in cp.sort_values('r1_eleitorado',ascending=False).iterrows()],
  FL=[r.nome for i,r in cp.iterrows() if r.lead1>0 and r.lead2<0],L1n=int((cp.lead1<0).sum()),L2n=int((cp.lead2<0).sum()))
# ---- fluxos (estimativas)
bf=json.load(open(ROOT/'dados/derivados/boot_flows.json'))
col=bf['col']; det=bf['det']
S['flow']=dict(col={k:col[k] for k in ['flows','rates','rates_lo','rates_hi','flows_lo','flows_hi']},det={k:det[k] for k in ['flows','rates','rates_lo','rates_hi']},B=col['B'])
S['dd']=pd.read_csv(ROOT/'dados/derivados/limites_duncan_davis.csv').to_dict('records')
# ---- comparecimento e brancos/nulos
z['bn1c']=z.bn1; 
def wcorr(x,y,w):
    mx=np.average(x,weights=w);my=np.average(y,weights=w); return float(np.average((x-mx)*(y-my),weights=w)/np.sqrt(np.average((x-mx)**2,weights=w)*np.average((y-my)**2,weights=w)))
def within(c):
    return z[c]-z.groupby('uf')[c].transform(lambda s: np.average(s,weights=z.loc[s.index,'w']))
z['dt']=z.t2-z.t1; z['dbn']=z.bn2-z.bn1; z['o1']=z.O1/z.r1_validos*100
S['corr']={c:dict(bruta=wcorr(z.dm,z[c],z.w),dentro=wcorr(within('dm'),within(c),z.w)) for c in ['m1','o1','bn1','dbn','dt','t1']}
z['qbn']=pd.qcut(z.bn1,5,labels=False)
qs=[]
for q in range(5):
    c=z[z.qbn==q]; qs.append(dict(q=q+1,bn1_lo=float(c.bn1.min()),bn1_hi=float(c.bn1.max()),bn1=float(np.average(c.bn1,weights=c.r1_comp)),dm=float(np.average(c.dm,weights=c.w)),dbn=float(np.average(c.dbn,weights=c.r2_comp)),n=len(c),m1=float(np.average(c.m1,weights=c.w))))
S['qbn']=qs
# quantis de dt
S['dt_q']=wq(z.dt,z.w,[.05,.25,.5,.75,.95])
# ---- variância
def decomp(col):
    w=z.w; mu_=np.average(z[col],weights=w); tot_=np.average((z[col]-mu_)**2,weights=w)
    muf=z.groupby('uf').apply(lambda g: np.average(g[col],weights=g.w)); a=z.uf.map(muf)
    mm=z.groupby('mun').apply(lambda g: np.average(g[col],weights=g.w)); b=z.mun.map(mm)
    return dict(sd=float(np.sqrt(tot_)),uf=float(np.average((a-mu_)**2,weights=w)/tot_*100),mun=float(np.average((b-a)**2,weights=w)/tot_*100),zona=float(np.average((z[col]-b)**2,weights=w)/tot_*100))
S['var']={c:decomp(c) for c in ['m1','m2','dm']}
# ---- cidades (faixa de margem por zona)
mt=z.groupby('mun').r1_eleitorado.sum().sort_values(ascending=False)
S['cities']=[]
for m in mt.index[:12]:
    c=z[z.mun==m]; tm=marg(pd.DataFrame([c[['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()])).iloc[0]
    S['cities'].append(dict(nome=c.municipio.iloc[0],uf=c.uf.iloc[0],nz=len(c),E=float(c.r1_eleitorado.sum()),m1=float(tm.m1),m2=float(tm.m2),dm=float(tm.dm),zmin=float(c.m2.min()),zmax=float(c.m2.max()),zones=[(int(r.zona),float(r.m1),float(r.m2),float(r.r1_eleitorado)) for r in c.itertuples()],nFL=int(((c.lead1>0)&(c.lead2<0)).sum()),swing=float(c.swing.sum()),dmmin=float(c.dm.min()),dmmax=float(c.dm.max())))
# exterior
ex=marg(pd.DataFrame([d[d.uf=='zz'][['F1','L1','F2','L2','O1','r1_validos','r2_validos','r1_comp','r2_comp','BN1','BN2','r1_eleitorado','r2_eleitorado','swing']].sum()])).iloc[0]; S['ext']={k:float(v) for k,v in ex.items()}
pv=z[z.m2.abs()<2]; S['pivot']=dict(n=len(pv),E=float(pv.r1_eleitorado.sum()),V=float(pv.r2_validos.sum()),share=float(pv.r2_validos.sum()/z.r2_validos.sum()*100))
json.dump(S,open(ROOT/'dados/derivados/estudos_stats.json','w'),ensure_ascii=False,default=lambda o: float(o) if isinstance(o,(np.floating,np.integer)) else str(o))
print('ok',len(json.dumps(S,default=str))/1e3,'KB')
