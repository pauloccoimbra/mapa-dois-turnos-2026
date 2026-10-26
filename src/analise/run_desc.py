import sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import numpy as np, pandas as pd
from lib import *
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 50)
d = load()
import pathlib, os
OUT = str(pathlib.Path(__file__).resolve().parents[2] / 'dados' / 'derivados') + '/'
os.makedirs(OUT, exist_ok=True)

def agg(df, by):
    g = df.groupby(by) if by else df.assign(_all='Brasil').groupby('_all')
    a = g[['r1_eleitorado', 'r2_eleitorado', 'r1_comp', 'r2_comp', 'r1_validos', 'r2_validos', 'r1_brancos', 'r1_nulos', 'r2_brancos', 'r2_nulos',
           'r1_c22', 'r1_c13', 'r1_outros', 'r2_c22', 'r2_c13', 'r1_c55', 'r1_c30', 'r1_c70', 'r1_c14', 'r1_minor']].sum()
    a['zonas'] = g.size()
    a['comp1'] = a.r1_comp / a.r1_eleitorado * 100; a['comp2'] = a.r2_comp / a.r2_eleitorado * 100
    a['d_comp'] = a.comp2 - a.comp1
    a['bn1'] = (a.r1_brancos + a.r1_nulos) / a.r1_comp * 100; a['bn2'] = (a.r2_brancos + a.r2_nulos) / a.r2_comp * 100
    a['d_bn'] = a.bn2 - a.bn1
    a['br1'] = a.r1_brancos / a.r1_comp * 100; a['br2'] = a.r2_brancos / a.r2_comp * 100
    a['nu1'] = a.r1_nulos / a.r1_comp * 100; a['nu2'] = a.r2_nulos / a.r2_comp * 100
    a['L1'] = a.r1_c13 / a.r1_validos * 100; a['F1'] = a.r1_c22 / a.r1_validos * 100; a['O1'] = a.r1_outros / a.r1_validos * 100
    a['L2'] = a.r2_c13 / a.r2_validos * 100; a['F2'] = a.r2_c22 / a.r2_validos * 100
    a['dL'] = a.L2 - a.L1; a['dF'] = a.F2 - a.F1
    a['m1'] = a.F1 - a.L1; a['m2'] = a.F2 - a.L2; a['d_m'] = a.m2 - a.m1
    a['dLv'] = a.r2_c13 - a.r1_c13; a['dFv'] = a.r2_c22 - a.r1_c22
    a['dBN'] = (a.r2_brancos + a.r2_nulos) - (a.r1_brancos + a.r1_nulos)
    a['dComp'] = a.r2_comp - a.r1_comp
    a['lider1'] = np.where(a.r1_c22 > a.r1_c13, 'Flávio', 'Lula'); a['lider2'] = np.where(a.r2_c22 > a.r2_c13, 'Flávio', 'Lula')
    return a

tabs = {}
tabs['brasil'] = agg(d, None)
tabs['regiao'] = agg(d, 'regiao')
tabs['uf'] = agg(d, 'UF')
tabs['mun'] = agg(d.assign(mun=d.UF + ' – ' + d.municipio, ), ['uf', 'cod_mun', 'municipio'])
for k, v in tabs.items(): v.to_csv(OUT + f'desc_{k}.csv')
print(tabs['brasil'].T.round(3).to_string())
print(tabs['regiao'][['zonas', 'r1_eleitorado', 'comp1', 'comp2', 'd_comp', 'bn1', 'bn2', 'd_bn', 'L1', 'F1', 'O1', 'L2', 'F2', 'dL', 'dF', 'm1', 'm2', 'd_m']].round(2).to_string())
print(tabs['uf'][['zonas', 'comp1', 'comp2', 'd_comp', 'bn1', 'bn2', 'd_bn', 'L1', 'F1', 'O1', 'L2', 'F2', 'dL', 'dF', 'm1', 'm2', 'd_m', 'lider1', 'lider2']].round(2).to_string())

# trocas de liderança (entre Lula e Flávio, por votos nominais de cada um)
zn = d.copy()
zn['lid1'] = np.where(zn.r1_c22 > zn.r1_c13, 'F', 'L'); zn['lid2'] = np.where(zn.r2_c22 > zn.r2_c13, 'F', 'L')
zn['troca'] = zn.lid1 != zn.lid2
print('zonas que trocaram de líder:', zn.troca.sum(), 'eleitorado', zn[zn.troca].E.sum())
print(zn.groupby(['lid1', 'lid2']).agg(n=('E', 'size'), E=('E', 'sum')))
mu = tabs['mun'].reset_index()
print('municípios que trocaram de líder:', (mu.lider1 != mu.lider2).sum(), 'de', len(mu))
print(pd.crosstab(mu.lider1, mu.lider2))
print(pd.crosstab(mu.uf, [mu.lider1, mu.lider2]))
# distribuição zona
def wq(x, w, qs):
    o = np.argsort(x); x = np.asarray(x)[o]; w = np.asarray(w)[o]; c = np.cumsum(w) / w.sum()
    return [x[np.searchsorted(c, q)] for q in qs]
zn['L1'] = zn.r1_c13 / zn.r1_validos * 100; zn['F1'] = zn.r1_c22 / zn.r1_validos * 100
zn['L2'] = zn.r2_c13 / zn.r2_validos * 100; zn['F2'] = zn.r2_c22 / zn.r2_validos * 100
zn['dL'] = zn.L2 - zn.L1; zn['dF'] = zn.F2 - zn.F1
zn['comp1'] = zn.r1_comp / zn.r1_eleitorado * 100; zn['comp2'] = zn.r2_comp / zn.r2_eleitorado * 100; zn['d_comp'] = zn.comp2 - zn.comp1
zn['bn1'] = zn.r1_bn / zn.r1_comp * 100; zn['bn2'] = zn.r2_bn / zn.r2_comp * 100; zn['d_bn'] = zn.bn2 - zn.bn1
zn['O1'] = zn.r1_outros / zn.r1_validos * 100
zn['abst1'] = 100 - zn.comp1
big = zn[zn.E >= 500]
for c in ['dL', 'dF', 'd_comp', 'd_bn']:
    print(c, 'q5,25,50,75,95 (pond.)', np.round(wq(big[c], big.E, [.05, .25, .5, .75, .95]), 2), 'zonas dL>0:' if c == 'dL' else '')
print('zonas (E>=500) com Lula subindo:', (big.dL > 0).mean(), ' Flávio subindo:', (big.dF > 0).mean(), ' ambos:', ((big.dL > 0) & (big.dF > 0)).mean())
print('zonas (todas) com comparecimento subindo:', (zn.d_comp > 0).mean(), ' BN caindo:', (zn.d_bn < 0).mean())
zn.to_csv(OUT + 'zonas_derivadas.csv', index=False)

# correlações ponderadas (zona e dentro da UF)
def wcorr(x, y, w):
    mx = np.average(x, weights=w); my = np.average(y, weights=w)
    cov = np.average((x - mx) * (y - my), weights=w); return cov / np.sqrt(np.average((x - mx) ** 2, weights=w) * np.average((y - my) ** 2, weights=w))
def wslope(x, y, w):
    mx = np.average(x, weights=w); my = np.average(y, weights=w)
    return np.sum(w * (x - mx) * (y - my)) / np.sum(w * (x - mx) ** 2)
def within(df, col):
    return df[col] - df.groupby('uf')[col].transform(lambda s: np.average(s, weights=df.loc[s.index, 'E']))
rows = []
z2 = zn[(zn.E >= 200) & (zn.uf != 'zz')].copy()
for (x, y, lab) in [('O1', 'dL', 'Δ Lula (p.p. válidos) × % outros candidatos 1T'), ('O1', 'dF', 'Δ Flávio × % outros candidatos 1T'),
                    ('abst1', 'd_comp', 'Δ comparecimento × abstenção 1T'), ('bn1', 'd_bn', 'Δ %BN × %BN 1T'),
                    ('d_comp', 'dL', 'Δ Lula × Δ comparecimento'), ('d_comp', 'dF', 'Δ Flávio × Δ comparecimento'),
                    ('L1', 'dL', 'Δ Lula × % Lula 1T'), ('F1', 'dF', 'Δ Flávio × % Flávio 1T')]:
    xx, yy, ww = z2[x].values, z2[y].values, z2.E.values
    xw, yw = within(z2.assign(), x).values, within(z2.assign(), y).values
    rows.append([lab, wcorr(xx, yy, ww), wslope(xx, yy, ww), wcorr(xw, yw, ww), wslope(xw, yw, ww)])
cor = pd.DataFrame(rows, columns=['relação', 'corr', 'inclinação', 'corr_dentro_UF', 'inclinação_dentro_UF'])
print(cor.round(3).to_string()); cor.to_csv(OUT + 'correlacoes.csv', index=False)

# limites determinísticos de Duncan–Davis (tabela 5x4, por zona e somados)
X, Y = mats_col(d)
lo = np.zeros((5, 4)); hi = np.zeros((5, 4))
for j in range(5):
    for k in range(4):
        tot = X.sum(1)  # soma das linhas na zona
        hi[j, k] = np.minimum(X[:, j], Y[:, k]).sum()
        lo[j, k] = np.maximum(0, X[:, j] + Y[:, k] - X.sum(1)).sum()
tot_row = X.sum(0)
bl = pd.DataFrame({'origem': np.repeat(ROWS_COL, 4), 'destino': np.tile(COLS_COL, 5), 'min_%linha': (lo / tot_row[:, None]).ravel() * 100, 'max_%linha': (hi / tot_row[:, None]).ravel() * 100,
                   'min_milhões': lo.ravel() / 1e6, 'max_milhões': hi.ravel() / 1e6})
print(bl.round(2).to_string()); bl.to_csv(OUT + 'limites_duncan_davis.csv', index=False)
