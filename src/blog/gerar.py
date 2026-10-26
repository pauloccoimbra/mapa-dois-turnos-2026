"""Gera os posts (HTML para Blogger), os gráficos em PNG e o guia de publicação."""
import sys, re, json, os, pathlib, asyncio, importlib, zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import base, posts_a, posts_b, posts_c, posts_d
OUT=pathlib.Path(__file__).resolve().parents[2]/'blog'; 
import shutil; shutil.rmtree(OUT,ignore_errors=True); (OUT/'posts').mkdir(parents=True); (OUT/'imagens').mkdir()
meta=[]; figs=[]
for p in sorted(base.POSTS,key=lambda x:x['num']):
    h=p['fn']()
    assert not re.search(r'\bnan\b|None|\{|\}|undefined',re.sub(r'<svg.*?</svg>','',h,flags=re.S)),p['num']
    fn=f"{p['num']:02d}-{p['slug']}"
    svgs=re.findall(r'<svg.*?</svg>',h,flags=re.S)
    # versão com PNG de reserva em arquivo separado; o HTML mantém SVG embutido
    (OUT/'posts'/f'{fn}.html').write_text(h,encoding='utf-8')
    for k,s in enumerate(svgs,1): figs.append((f'{fn}-fig{k}.png',s))
    meta.append(dict(num=p['num'],file=fn+'.html',title=p['title'],desc=p['desc'],labels=p['labels'],chars=len(h),nfig=len(svgs)))
    assert len(p['desc'])<=150,(p['num'],len(p['desc']))
from playwright.async_api import async_playwright
async def png():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(device_scale_factor=2,viewport={'width':620,'height':800})
        for name,s in figs:
            await pg.set_content('<body style="margin:0;background:#fff">'+s.replace('width="100%"','width="520"')+'</body>')
            el=await pg.query_selector('svg'); await el.screenshot(path=str(OUT/'imagens'/name))
        await b.close()
asyncio.run(png())
# guia no formato Boletim e instruções de publicação (escritos à mão)
shutil.copy(pathlib.Path(__file__).parent/'static'/'00-guia-da-serie.html',OUT/'posts'/'00-guia-da-serie.html')
shutil.copy(pathlib.Path(__file__).parent/'static'/'README_BLOGGER.md',OUT/'README_BLOGGER.md')
# previa completa
pv='<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Prévia da série</title><body style="background:#fff;max-width:680px;margin:0 auto;padding:16px;font-family:Georgia,serif">'
for m in meta: pv+=f"<h1 style='font-size:26px;line-height:1.25'>{m['title']}</h1>"+(OUT/'posts'/m['file']).read_text(encoding='utf-8')+'<hr style="margin:40px 0">'
(OUT/'previa.html').write_text(pv,encoding='utf-8')
json.dump(meta,open(OUT/'meta.json','w'),ensure_ascii=False,indent=1)
print([ (m['num'],m['chars'],m['nfig']) for m in meta],len(figs))
