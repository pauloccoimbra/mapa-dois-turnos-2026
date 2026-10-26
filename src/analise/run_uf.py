import sys, json, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import numpy as np, pandas as pd
from lib import *
from multiprocessing import Pool
d = load()
import pathlib, os
OUT = str(pathlib.Path(__file__).resolve().parents[2] / 'dados' / 'derivados') + '/'
os.makedirs(OUT, exist_ok=True)
Xc, Yc = mats_col(d); Xd, Yd = mats_det(d); E = d.E.values.astype(float)
Pn_c = fit_P(Xc, Yc, E); Pn_d = fit_P(Xd, Yd, E)
reg_ix = d.groupby('regiao').indices; uf_ix = d.groupby('uf').indices
Preg_c = {r: fit_P(Xc[ix], Yc[ix], E[ix], prior=Pn_c, kappa=50) for r, ix in reg_ix.items()}
Preg_d = {r: fit_P(Xd[ix], Yd[ix], E[ix], prior=Pn_d, kappa=50) for r, ix in reg_ix.items()}
Puf_c = {u: fit_P(Xc[ix], Yc[ix], E[ix], prior=Preg_c[d.regiao.iloc[ix[0]]], kappa=30) for u, ix in uf_ix.items()}

def boot_unit(args):
    kind, name, seed, B = args
    rng = np.random.default_rng(seed)
    if kind == 'uf':
        ix = uf_ix[name]; prior = Preg_c[d.regiao.iloc[ix[0]]]; kap = 30; X, Y = Xc, Yc
    elif kind == 'reg':
        ix = reg_ix[name]; prior = Pn_c; kap = 50; X, Y = Xc, Yc
    else:
        ix = reg_ix[name]; prior = Pn_d; kap = 50; X, Y = Xd, Yd
    sub = d.iloc[ix]; mk = sub.mun_key.values
    um = pd.unique(mk); pos = {m: ix[np.where(mk == m)[0]] for m in um}
    outs = []
    for b in range(B):
        ks = rng.choice(um, size=len(um), replace=True)
        ii = np.concatenate([pos[k] for k in ks])
        P = fit_P(X[ii], Y[ii], E[ii], prior=prior, kappa=kap)
        outs.append(P)
    outs = np.array(outs)
    return (kind, name, np.percentile(outs, 2.5, axis=0), np.percentile(outs, 97.5, axis=0))

if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    jobs = [('uf', u, 7 + i, B) for i, u in enumerate(uf_ix)] + [('reg', r, 77 + i, B) for i, r in enumerate(reg_ix)] + [('regdet', r, 177 + i, B) for i, r in enumerate(reg_ix)]
    t = time.time()
    with Pool(2) as p: res = p.map(boot_unit, jobs)
    print('boot', time.time() - t, flush=True)
    rows = []
    def add(level, name, ix, X, P, lo, hi, R, C):
        tot = X[ix].sum(0)
        for j, rj in enumerate(R):
            for k, ck in enumerate(C):
                rows.append([level, name, rj, ck, P[j, k], lo[j, k], hi[j, k], P[j, k] * tot[j], tot[j], len(ix)])
    for kind, name, lo, hi in res:
        if kind == 'uf':
            add('uf', name.upper(), uf_ix[name], Xc, Puf_c[name], lo, hi, ROWS_COL, COLS_COL)
        elif kind == 'reg':
            add('regiao', name, reg_ix[name], Xc, Preg_c[name], lo, hi, ROWS_COL, COLS_COL)
        else:
            add('regiao_det', name, reg_ix[name], Xd, Preg_d[name], lo, hi, ROWS_DET, COLS_DET)
    df = pd.DataFrame(rows, columns=['nivel', 'unidade', 'origem', 'destino', 'taxa', 'lo', 'hi', 'fluxo', 'base_origem', 'n_zonas'])
    df.to_csv(OUT + 'transferencias.csv', index=False)
    # R2 por nível
    q = []
    for u, ix in uf_ix.items(): q.append(['uf', u.upper()] + list(fit_quality(Xc[ix], Yc[ix], E[ix], Puf_c[u])))
    for r, ix in reg_ix.items(): q.append(['regiao', r] + list(fit_quality(Xc[ix], Yc[ix], E[ix], Preg_c[r])))
    q.append(['brasil', 'nacional'] + list(fit_quality(Xc, Yc, E, Pn_c)))
    pd.DataFrame(q, columns=['nivel', 'unidade'] + ['R2_' + c for c in COLS_COL]).to_csv(OUT + 'ajuste_r2.csv', index=False)
    # fluxos nacionais por especificação (P nacional único, P regional, P por UF)
    def tot_flows(Pd, ixd, X): return sum(Pd[g] * X[ix].sum(0)[:, None] for g, ix in ixd.items())
    specs = {'P nacional único': Pn_c * Xc.sum(0)[:, None], 'P por região': tot_flows(Preg_c, reg_ix, Xc), 'P por UF': tot_flows(Puf_c, uf_ix, Xc)}
    json.dump({k: v.tolist() for k, v in specs.items()}, open(OUT + 'fluxos_especificacoes.json', 'w'))
    print('ok')
