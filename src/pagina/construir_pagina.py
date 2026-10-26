"""Constrói index.html: junta dados por zona, estimativas, malhas e o modelo de página (template.html).
Uso (na raiz do repositório): python3 src/pagina/construir_pagina.py"""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src' / 'analise'))
import pandas as pd
from lib import load
DER = ROOT / 'dados' / 'derivados'; GEO = ROOT / 'dados' / 'geo'
d = load()
t = pd.read_csv(DER / 'transferencias.csv')
O = ['Flávio','Lula','Outros cand.','Brancos+Nulos','Abstenção']; D = ['Lula','Flávio','Brancos+Nulos','Abstenção']
def mats(level):
    res = {}
    for u, g in t[t.nivel==level].groupby('unidade'):
        m = {}
        for o in O:
            gg = g[g.origem==o].set_index('destino')
            m[o] = {'base': float(gg.base_origem.iloc[0]), 'n': int(gg.n_zonas.iloc[0]),
                    'r': [round(float(gg.loc[x,'taxa']),4) for x in D], 'lo': [round(float(gg.loc[x,'lo']),4) for x in D], 'hi':[round(float(gg.loc[x,'hi']),4) for x in D]}
        res[u] = m
    return res
est = {'uf': mats('uf'), 'regiao': mats('regiao')}
muns = {}
for (uf, cm), g in d.groupby(['uf','cod_mun'], sort=False):
    ib = None if pd.isna(g.cod_ibge.iloc[0]) else int(g.cod_ibge.iloc[0])
    zs = [[int(r.zona), int(r.r1_eleitorado), int(r.r1_comp), int(r.r1_brancos), int(r.r1_nulos), int(r.r1_validos), int(r.r1_c22), int(r.r1_c13),
           int(r.r2_eleitorado), int(r.r2_comp), int(r.r2_brancos), int(r.r2_nulos), int(r.r2_validos), int(r.r2_c22), int(r.r2_c13)] for r in g.itertuples()]
    muns.setdefault(uf, []).append([ib, g.municipio.iloc[0], int(cm), zs])
ufreg = d.groupby('uf').regiao.first().to_dict()
out = {'muns': muns, 'ufreg': ufreg, 'est': est}
bf = json.load(open(DER / 'boot_flows.json'))['col']
br = {}
for i,o in enumerate(O):
    br[o] = {'base': float(sum(bf['flows'][i])), 'n': int(len(d)),
             'r': [round(x,4) for x in bf['rates'][i]], 'lo': [round(x,4) for x in bf['rates_lo'][i]], 'hi': [round(x,4) for x in bf['rates_hi'][i]]}
out['est']['br'] = br
cen = {}
for f in 'abcdefghi':
    cen.update(json.load(open(GEO / 'centroides' / f'cen_{f}.json')))
out['geo'] = {'uf': json.load(open(GEO / 'malha_uf.json')), 'cen': cen, 'mun': json.load(open(GEO / 'malha_municipal_simplificada.json'))}
assert sorted(cen.keys()) == sorted(out['geo']['uf'].keys())
data = json.dumps(out, ensure_ascii=False, separators=(',',':'))
tpl = (ROOT / 'src' / 'pagina' / 'template.html').read_text(encoding='utf-8')
head = ('<!doctype html>\n<html lang="pt-BR">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="description" content="Mapa interativo da eleição presidencial de 2026 (1º e 2º turnos) por região, estado, município e zona eleitoral. Dados do TSE.">\n')
html = head + tpl.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','').replace('/*DATA*/', data) + '\n</html>\n'
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print('index.html', round(len(html)/1e6,2), 'MB')
print('totais:', d[['r1_c22','r1_c13','r2_c22','r2_c13','r1_eleitorado','r2_comp']].sum().to_dict())
