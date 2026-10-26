import sys, json, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import numpy as np, pandas as pd
from lib import *
from multiprocessing import Pool

d = load()
import pathlib, os
OUT = str(pathlib.Path(__file__).resolve().parents[2] / 'dados' / 'derivados') + '/'
os.makedirs(OUT, exist_ok=True)
import os; os.makedirs(OUT, exist_ok=True)

def reg_flows(dd, mats, kappa_reg=50):
    X, Y = mats(dd); E = dd.E.values.astype(float)
    Pn = fit_P(X, Y, E)
    tot = 0
    for r, ix in dd.groupby('regiao').indices.items():
        Pr = fit_P(X[ix], Y[ix], E[ix], prior=Pn, kappa=kappa_reg)
        tot = tot + Pr * X[ix].sum(0)[:, None]
    return Pn, tot

def one_boot(args):
    which, seed = args
    rng = np.random.default_rng(seed)
    mats = mats_col if which == 'col' else mats_det
    parts = []
    for r, sub in d.groupby('regiao'):
        keys = sub.mun_key.unique()
        ks = rng.choice(keys, size=len(keys), replace=True)
        idx = sub.groupby('mun_key').indices
        ii = np.concatenate([sub.iloc[idx[k]].index.values for k in ks])
        parts.append(d.loc[ii])
    bd = pd.concat(parts, ignore_index=True)
    Pn, F = reg_flows(bd, mats)
    return Pn, F

if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    res = {}
    for which, mats in [('col', mats_col), ('det', mats_det)]:
        t = time.time()
        Pn0, F0 = reg_flows(d, mats)
        with Pool(2) as p:
            outs = p.map(one_boot, [(which, 1000 + b) for b in range(B)])
        Pn_b = np.array([o[0] for o in outs]); F_b = np.array([o[1] for o in outs])
        # taxas (linhas normalizadas) a partir dos fluxos
        R_b = F_b / F_b.sum(2, keepdims=True)
        R0 = F0 / F0.sum(1, keepdims=True)
        res[which] = {
            'flows': F0.tolist(), 'rates': R0.tolist(),
            'rates_lo': np.percentile(R_b, 2.5, axis=0).tolist(), 'rates_hi': np.percentile(R_b, 97.5, axis=0).tolist(),
            'flows_lo': np.percentile(F_b, 2.5, axis=0).tolist(), 'flows_hi': np.percentile(F_b, 97.5, axis=0).tolist(),
            'Pnat': Pn0.tolist(), 'Pnat_lo': np.percentile(Pn_b, 2.5, axis=0).tolist(), 'Pnat_hi': np.percentile(Pn_b, 97.5, axis=0).tolist(),
            'B': B, 'secs': time.time() - t}
        print(which, 'done', time.time() - t, flush=True)
    json.dump(res, open(OUT + 'boot_flows.json', 'w'))
