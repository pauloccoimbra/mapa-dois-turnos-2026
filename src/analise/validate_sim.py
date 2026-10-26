import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import numpy as np, pandas as pd
from lib import *

# Validação do estimador: gera dados com matriz de transição conhecida (heterogênea por região), reusa as composições
# reais de 1º turno (X) e ruído multinomial, e verifica se o ajuste (nacional e hierárquico) recupera a matriz verdadeira.
d = load(); E = d.E.values.astype(float)
X, Y = mats_col(d)
rng = np.random.default_rng(42)
Ptrue_nat = np.array([[0.003, 0.99, 0.004, 0.003],
                      [0.997, 0.0, 0.0, 0.003],
                      [0.40, 0.44, 0.155, 0.005],
                      [0.60, 0.05, 0.30, 0.05],     # B/N -> verdade diferente do que o modelo estimou (para testar a recuperação)
                      [0.05, 0.01, 0.04, 0.90]])
Ptrue_nat = Ptrue_nat / Ptrue_nat.sum(1, keepdims=True)

def simulate(het):
    Ys = np.zeros_like(Y)
    for r, ix in d.groupby('regiao').indices.items():
        P = Ptrue_nat.copy()
        if het:  # desloca Demais -> Lula/Flávio por região (+-5 p.p.) e B/N -> Lula (+-10 p.p.)
            s = rng.uniform(-0.05, 0.05); P[2, 0] += s; P[2, 1] -= s
            t = rng.uniform(-0.10, 0.10); P[3, 0] += t; P[3, 2] -= t
            P = np.clip(P, 0, None); P = P / P.sum(1, keepdims=True)
        for i in ix:
            for j in range(5):
                n = int(X[i, j])
                if n > 0: Ys[i] += rng.multinomial(n, P[j])
    return Ys

for het in [False, True]:
    Ys = simulate(het)
    dd = d.copy()
    Pn = fit_P(X, Ys, E)
    h = {}
    tot = 0
    for r, ix in d.groupby('regiao').indices.items():
        Pr = fit_P(X[ix], Ys[ix], E[ix], prior=Pn, kappa=50)
        tot = tot + Pr * X[ix].sum(0)[:, None]
    est = tot / tot.sum(1, keepdims=True)
    # verdade agregada (com heterogeneidade) = taxa efetiva
    print('heterogêneo' if het else 'homogêneo')
    print(' nacional estimado (linhas = origem, colunas = Lula, Flávio, B/N, Abst.):')
    print(pd.DataFrame(Pn, index=ROWS_COL, columns=COLS_COL).round(3).to_string())
    print(' hierárquico (região) agregado:')
    print(pd.DataFrame(est, index=ROWS_COL, columns=COLS_COL).round(3).to_string())
    # verdade agregada
    # fluxos verdadeiros agregados: usar Ys e X não identifica; comparar com Ptrue_nat em média
print('verdade (média):')
print(pd.DataFrame(Ptrue_nat, index=ROWS_COL, columns=COLS_COL).round(3).to_string())
