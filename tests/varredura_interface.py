import asyncio,random,sys
from playwright.async_api import async_playwright
import pathlib
f=sys.argv[1] if len(sys.argv)>1 else str(pathlib.Path(__file__).resolve().parents[1]/'index.html')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for scheme in ['light','dark']:
            pg=await b.new_page(viewport={'width':1280,'height':900},color_scheme=scheme)
            errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
            await pg.goto('file://'+f); await pg.wait_for_timeout(400)
            keys=await pg.evaluate("Object.keys(__app.units)")
            nonmun=[k for k in keys if k[0] in 'bru']
            muns=[k for k in keys if k[0]=='m']
            random.seed(1); sample=nonmun+random.sample(muns,250 if scheme=='light' else 60)
            bad=[]
            for met in (['m2','m1','dm','t2','dt','bn2','dbn'] if scheme=='light' else ['m2','t2']):
                await pg.select_option('#metric',met)
                for k in (nonmun if met!='m2' else sample):
                    await pg.evaluate(f"__app.go('{k}')")
                    t=await pg.evaluate("document.body.innerText")
                    for w in ['NaN','undefined','Infinity','null']:
                        if w in t: bad.append((met,k,w))
                    if k.startswith('m:'):
                        r=await pg.evaluate("(()=>{const rs=[...document.querySelectorAll('#zsvg rect')];const a=rs.reduce((s,r)=>s+ +r.getAttribute('width')* +r.getAttribute('height'),0);return [rs.length,a]})()")
                        u=await pg.evaluate(f"__app.units['{k}'].children.length")
                        if r[0]!=u or abs(r[1]-400*(await pg.evaluate("+document.querySelector('#zsvg').viewBox.baseVal.height")))>1: bad.append(('tree',k,r,u))
            print(scheme,'bad',bad[:10],len(bad),'errs',errs[:5])
            await pg.close()
        await b.close()
asyncio.run(main())
