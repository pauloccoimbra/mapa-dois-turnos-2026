import numpy as np, pandas as pd
from scipy.optimize import minimize

REG = {
 'ac':'Norte','am':'Norte','ap':'Norte','pa':'Norte','ro':'Norte','rr':'Norte','to':'Norte',
 'al':'Nordeste','ba':'Nordeste','ce':'Nordeste','ma':'Nordeste','pb':'Nordeste','pe':'Nordeste','pi':'Nordeste','rn':'Nordeste','se':'Nordeste',
 'df':'Centro-Oeste','go':'Centro-Oeste','mt':'Centro-Oeste','ms':'Centro-Oeste',
 'es':'Sudeste','mg':'Sudeste','rj':'Sudeste','sp':'Sudeste',
 'pr':'Sul','rs':'Sul','sc':'Sul',
 'zz':'Exterior'}
CAND = {'r1_c22':'Flávio Bolsonaro','r1_c13':'Lula','r1_c55':'Caiado','r1_c30':'Zema','r1_c70':'Cury','r1_c14':'Renan Santos'}
MINOR = ['r1_c16','r1_c21','r1_c27','r1_c29','r1_c35','r1_c80']

def load(path=None):
    import pathlib
    path = path or pathlib.Path(__file__).resolve().parents[2] / 'dados' / 'zonas_2026_t1_t2.csv'
    d = pd.read_csv(path)
    d['regiao'] = d.uf.map(REG)
    d['mun_key'] = d.uf + '_' + d.cod_mun.astype(str).str.zfill(5)
    d['UF'] = d.uf.str.upper()
    d['r1_minor'] = d[MINOR].sum(axis=1)
    d['r1_outros'] = d.r1_c55 + d.r1_c30 + d.r1_c70 + d.r1_c14 + d.r1_minor
    d['r1_bn'] = d.r1_brancos + d.r1_nulos
    d['r2_bn'] = d.r2_brancos + d.r2_nulos
    d['E'] = d.r1_eleitorado
    d['r1_abst'] = d.r1_eleitorado - d.r1_comp
    d['r2_abst_E1'] = d.r1_eleitorado - d.r2_comp     # abstenção do 2º turno medida sobre o eleitorado do 1º (preserva identidade contábil)
    d['r2_abst'] = d.r2_eleitorado - d.r2_comp
    return d

# categorias de origem (1º turno) e destino (2º turno)
ROWS_DET = ['Flávio','Lula','Caiado','Zema','Cury','Renan Santos','Demais cand.','Brancos','Nulos','Abstenção']
COLS_DET = ['Lula','Flávio','Brancos','Nulos','Abstenção']
ROWS_COL = ['Flávio','Lula','Outros cand.','Brancos+Nulos','Abstenção']
COLS_COL = ['Lula','Flávio','Brancos+Nulos','Abstenção']

def mats_det(d):
    X = np.column_stack([d.r1_c22, d.r1_c13, d.r1_c55, d.r1_c30, d.r1_c70, d.r1_c14, d.r1_minor, d.r1_brancos, d.r1_nulos, d.r1_abst]).astype(float)
    Y = np.column_stack([d.r2_c13, d.r2_c22, d.r2_brancos, d.r2_nulos, d.r2_abst_E1]).astype(float)
    return X, Y

def mats_col(d):
    X = np.column_stack([d.r1_c22, d.r1_c13, d.r1_outros, d.r1_bn, d.r1_abst]).astype(float)
    Y = np.column_stack([d.r2_c13, d.r2_c22, d.r2_bn, d.r2_abst_E1]).astype(float)
    return X, Y

def fit_P(X, Y, E, constrained=True, P0=None, prior=None, kappa=0.0):
    """Mínimos quadrados ponderados (peso 1/E_i nos erros de contagem = pesos E_i na formulação em proporções do eleitorado).
    Restrições: P >= 0 e cada linha soma 1."""
    w = 1.0 / np.maximum(E, 1.0)
    A = (X * w[:, None]).T @ X
    B = (X * w[:, None]).T @ Y
    J, K = B.shape
    if not constrained:
        return np.linalg.lstsq(A, B, rcond=None)[0]
    scale = np.trace(A) / J
    A_, B_ = A / scale, B / scale
    lam = 0.0
    if prior is not None and kappa > 0:
        # kappa = nº de "unidades médias" de informação atribuídas ao prior (encolhimento parcial)
        lam = kappa * (np.trace(A) / J / len(E)) / scale
    def f(p):
        P = p.reshape(J, K)
        v = float(np.sum(P * (A_ @ P)) - 2 * np.sum(P * B_))
        if lam > 0: v += lam * float(np.sum((P - prior) ** 2))
        return v
    def g(p):
        P = p.reshape(J, K)
        gr = 2 * (A_ @ P) - 2 * B_
        if lam > 0: gr = gr + 2 * lam * (P - prior)
        return gr.ravel()
    cons = [{'type': 'eq', 'fun': lambda p, j=j: p.reshape(J, K)[j].sum() - 1,
             'jac': (lambda p, j=j: np.eye(J)[j][:, None].repeat(K, 1).ravel())} for j in range(J)]
    if P0 is None:
        P0 = prior.copy() if prior is not None else np.full((J, K), 1.0 / K)
    res = minimize(f, P0.ravel(), jac=g, bounds=[(0, 1)] * (J * K), constraints=cons, method='SLSQP',
                   options={'maxiter': 500, 'ftol': 1e-12})
    P = res.x.reshape(J, K)
    P = np.clip(P, 0, 1); P = P / P.sum(1, keepdims=True)
    return P

def boot_P(d, mats, B=200, seed=1, constrained=True, key='mun_key'):
    rng = np.random.default_rng(seed)
    groups = {k: ix.values for k, ix in d.groupby(key).indices.items()} if False else None
    idx_by = d.groupby(key).indices
    keys = np.array(list(idx_by.keys()))
    X, Y = mats(d); E = d.E.values.astype(float)
    P0 = fit_P(X, Y, E, constrained)
    out = []
    for b in range(B):
        ks = rng.choice(keys, size=len(keys), replace=True)
        ii = np.concatenate([idx_by[k] for k in ks])
        out.append(fit_P(X[ii], Y[ii], E[ii], constrained, P0=P0))
    out = np.array(out)
    return P0, np.percentile(out, 2.5, axis=0), np.percentile(out, 97.5, axis=0), out

def fit_quality(X, Y, E, P):
    """R2 ponderado de cada coluna prevista (nas proporções do eleitorado)."""
    w = E
    xs = X / E[:, None]; ys = Y / E[:, None]
    pred = xs @ P
    r2 = []
    for k in range(Y.shape[1]):
        m = np.average(ys[:, k], weights=w)
        sst = np.sum(w * (ys[:, k] - m) ** 2); sse = np.sum(w * (ys[:, k] - pred[:, k]) ** 2)
        r2.append(1 - sse / sst if sst > 0 else np.nan)
    return np.array(r2)


MAIN_REG = ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul']

def hier_fit(d, mats, kappa_reg=50, kappa_uf=30, level='uf'):
    """Ajuste hierárquico: P nacional -> P por região (encolhida ao nacional) -> P por UF (encolhida à região).
    Devolve dicionário com P por nível e fluxos (contagens) agregados."""
    X, Y = mats(d); E = d.E.values.astype(float)
    Pn = fit_P(X, Y, E)
    out = {'nat': Pn, 'reg': {}, 'uf': {}}
    for r, ix in d.groupby('regiao').indices.items():
        out['reg'][r] = fit_P(X[ix], Y[ix], E[ix], prior=Pn, kappa=kappa_reg)
    if level == 'uf':
        for u, ix in d.groupby('uf').indices.items():
            r = d.regiao.iloc[ix[0]]
            out['uf'][u] = fit_P(X[ix], Y[ix], E[ix], prior=out['reg'][r], kappa=kappa_uf)
    return out

def flows(d, mats, Pdict):
    """Fluxos (nº de eleitores) origem x destino somando P_g * X_g sobre os grupos g."""
    X, Y = mats(d)
    tot = None
    for g, ix in Pdict['groups'].items():
        F = Pdict['P'][g] * X[ix].sum(0)[:, None]
        tot = F if tot is None else tot + F
    return tot
