import asyncio, json, pathlib, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]
from playwright.async_api import async_playwright
uf=pd.read_csv(ROOT/'dados/derivados/desc_uf.csv'); mun=pd.read_csv(ROOT/'dados/derivados/desc_mun.csv'); print(uf.columns.tolist()[:5], len(mun))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':900})
        await pg.goto('file://'+str(ROOT/'index.html')); await pg.wait_for_timeout(500)
        res=await pg.evaluate("""()=>{const o={uf:{},mun:{}};for(const k in __app.units){const u=__app.units[k];if(u.level==='uf')o.uf[u.uf]=[u.a[6],u.a[7],u.a[13],u.a[14],u.a[2],u.a[9],u.a[3]+u.a[4],u.a[10]+u.a[11]];if(u.level==='mun')o.mun[u.uf+':'+u.key.split(':')[2]]=[u.a[6],u.a[7],u.a[13],u.a[14]]}return o}""")
        bad=0
        u=uf.set_index(uf.columns[0])
        for k,v in res['uf'].items():
            r=u.loc[k.upper()] if k.upper() in u.index else None
            if r is None: print('missing',k); bad+=1; continue
            exp=[r.r1_c22,r.r1_c13,r.r2_c22,r.r2_c13,r.r1_comp,r.r2_comp,r.r1_brancos+r.r1_nulos,r.r2_brancos+r.r2_nulos]
            if any(abs(a-b)>0.5 for a,b in zip(v,exp)): print('DIFF',k,v,exp); bad+=1
        m=mun.copy(); m['key']=m.uf+':'+m.cod_mun.astype(str)
        mm=m.set_index('key')
        for k,v in res['mun'].items():
            r=mm.loc[k]; exp=[r.r1_c22,r.r1_c13,r.r2_c22,r.r2_c13]
            if any(abs(a-b)>0.5 for a,b in zip(v,exp)): print('DIFFM',k,v,exp); bad+=1
        print('uf',len(res['uf']),'mun',len(res['mun']),'divergencias',bad); assert bad==0
        await b.close()
asyncio.run(main())
