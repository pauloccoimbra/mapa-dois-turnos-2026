# Dicionário de dados

## `dados/zonas_2026_t1_t2.csv`

Uma linha por município × zona eleitoral. Fonte: TSE, arquivos de divulgação de resultados, totalização por zona (lidos em 26/10/2026).

| Coluna | Descrição |
|---|---|
| `uf` | Sigla da UF em minúsculas; `zz` = exterior |
| `cod_mun` | Código do município no TSE (texto com zeros à esquerda) |
| `cod_ibge` | Código IBGE de 7 dígitos; vazio para o exterior (186 linhas) |
| `municipio` | Nome do município ou da localidade no exterior |
| `zona` | Número da zona eleitoral |
| `r1_eleitorado`, `r2_eleitorado` | Eleitorado apto no 1º e no 2º turno |
| `r1_comp`, `r2_comp` | Comparecimento |
| `r1_brancos`, `r1_nulos`, `r2_brancos`, `r2_nulos` | Votos brancos e nulos |
| `r1_validos`, `r2_validos` | Votos válidos |
| `r1_c22` | Flávio Bolsonaro, 1º turno |
| `r1_c13` | Lula, 1º turno |
| `r1_c55`, `r1_c30`, `r1_c70`, `r1_c14` | Caiado, Zema, Cury e Renan Santos, 1º turno |
| `r1_c16`, `r1_c21`, `r1_c27`, `r1_c29`, `r1_c35`, `r1_c80` | Demais candidatos, 1º turno (número do candidato) |
| `r2_c13`, `r2_c22` | Lula e Flávio Bolsonaro, 2º turno |

Os sufixos numéricos de `r1_c..` e `r2_c..` são os números dos candidatos na urna.

## `dados/derivados/`

| Arquivo | Conteúdo |
|---|---|
| `desc_brasil.csv`, `desc_regiao.csv`, `desc_uf.csv`, `desc_mun.csv` | Somas e indicadores por nível: `comp1/comp2` (comparecimento, %), `bn1/bn2` (brancos + nulos, % dos comparecentes), `L1/F1/L2/F2` (% dos válidos), `m1/m2` (margem Flávio − Lula, p.p.), `d_m` (mudança da margem), `lider1/lider2` |
| `zonas_derivadas.csv` | Base por zona com indicadores derivados (`troca` indica mudança de líder, `dL`/`dF` variações, `abst1`, `r2_abst_E1`, etc.) |
| `transferencias.csv` | Matrizes de migração por nível (`regiao`, `uf`; o nível Brasil está em `boot_flows.json`): `taxa`, intervalo `lo`–`hi`, `fluxo` (eleitores), `base_origem`, `n_zonas` |
| `boot_flows.json` | Resultado do bootstrap nacional (fluxos, taxas, percentis; 5×4 em `col` e detalhado em `det`) |
| `ajuste_r2.csv` | R² ponderado do ajuste por unidade e destino |
| `limites_duncan_davis.csv` | Limites determinísticos de cada célula da matriz nacional |
| `correlacoes.csv` | Correlações e inclinações entre variações e composição do 1º turno |
| `fluxos_especificacoes.json` | Matrizes nacionais sob especificações alternativas |

## `dados/geo/`

| Arquivo | Conteúdo |
|---|---|
| `malha_municipal_simplificada.json` | `{código da UF: [[código IBGE, "dx,dy dx,dy ...|anel2"], ...]}`; coordenadas em passos de 1/250 grau, codificadas por deltas; anéis separados por `|` (preenchimento par-ímpar) |
| `malha_uf.json` | Contornos das UFs no mesmo formato, por código da UF |
| `centroides/cen_*.json` | Centroides dos municípios (id em delta, x, y) usados quando falta polígono |
