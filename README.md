# Mapa dos Dois Turnos 2026

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
<!-- Troque XXXXXXX pelo número do DOI depois da primeira release (ver docs/PUBLICAR_ZENODO.md). -->

Mapa interativo da eleição presidencial de 2026 (1º e 2º turnos; Lula × Flávio Bolsonaro no 2º turno) por **região, estado, município e zona eleitoral**, com dados de divulgação do TSE, malhas municipais do IBGE e estimativas de migração de votos entre os turnos.

**Página:** <https://pauloccoimbra.github.io/mapa-dois-turnos-2026/> (ou abra `index.html` direto no navegador; não precisa de servidor nem de internet).

> **English summary.** Interactive, self-contained web map of Brazil's 2026 presidential election (first round and runoff) at region, state, municipality and electoral-zone level, built from TSE (Superior Electoral Court) open results and IBGE municipal boundaries. It includes ecological-inference estimates of how first-round voters moved between candidates, blank/null votes and abstention. Data, code and methodology are included; the repository is archived on Zenodo.

## O que a página mostra

- **Mapa por níveis:** Brasil → região → estado → município. No nível estadual, cada polígono é um município (5.564 polígonos). Clicar abre a unidade; as migalhas de pão voltam.
- **Cor do mapa** (seletor): margem Flávio − Lula no 1º e no 2º turno, mudança da margem, comparecimento, mudança no comparecimento, brancos + nulos e sua mudança.
- **Zonas eleitorais:** ao abrir um município, cada zona aparece como um bloco proporcional ao eleitorado (esquema, sem posição geográfica) e em tabela, com a etiqueta "virou" quando o líder mudou do 1º para o 2º turno. As zonas não têm malha pública; o esquema é só um arranjo.
- **Painel** com votos, percentuais, variações, brancos, nulos e comparecimento de cada unidade.
- **Migração de votos** (Brasil, regiões e estados): para onde foram os eleitores de cada origem do 1º turno, com faixas de 95%. São estimativas estatísticas, não observações; abaixo do nível de estado não são exibidas.
- Tema claro e escuro, uso no celular, sem cookies; única requisição externa: contagem anônima de visitas (GoatCounter).

## Resultados em uma linha

Brasil, 2º turno: Lula 64.256.232 votos (51,8% dos válidos) e Flávio Bolsonaro 59.826.041 (48,2%). Comparecimento de 78,9% para 80,8%. As estimativas indicam que quase todos os eleitores de cada finalista no 1º turno permaneceram com ele (Lula 99,7%; Flávio 98,9%) e que a troca direta entre os dois foi muito pequena (Flávio → Lula 0,4%, IC 95% 0,3–0,5%). O deslocamento da margem vem sobretudo do destino dos eleitores de outros candidatos, dos brancos e nulos e da abstenção. Ver `docs/METODOLOGIA.md` para o método, a validação por simulação e as limitações.

## Estrutura do repositório

```
index.html                       página pronta (dados e malhas embutidos, ~2,4 MB)
dados/
  zonas_2026_t1_t2.csv           base por município × zona (6.292 linhas), 1º e 2º turnos
  derivados/                     tabelas descritivas e estimativas (CSV/JSON)
  geo/                           malhas UF e municipal simplificadas, centroides
src/
  analise/                       estimador, descritivas, bootstrap, validação por simulação
  pagina/                        modelo da página, construtor do index.html, tratamento das malhas
tests/                           conferência dos totais e varredura da interface
docs/                            metodologia, dicionário de dados, passo a passo do Zenodo
```

## Como reproduzir

Requer Python 3.10+.

```bash
pip install -r requirements.txt
python3 src/analise/run_desc.py        # descritivas por Brasil, região, UF, município e zona
python3 src/analise/run_est.py 150     # bootstrap nacional (150 réplicas; demora)
python3 src/analise/run_uf.py 100      # matrizes por região e UF (100 réplicas; demora)
python3 src/analise/validate_sim.py    # validação do estimador por simulação
python3 src/pagina/construir_pagina.py # gera index.html
python3 tests/verificar_totais.py      # compara a página com as tabelas (requer playwright)
```

Série de posts (opcional): `python3 src/blog/estudos.py && python3 src/blog/gerar.py` (reescreve `blog/`; os PNGs requerem playwright).

Para refazer as malhas: `python3 src/pagina/baixar_malhas.py` e `python3 src/pagina/simplificar_malhas.py 0.008 250`.
`run_desc.py` e o construtor da página são determinísticos e reproduzem os arquivos versionados byte a byte. Os bootstraps usam sementes fixas.

## Fontes

- **Votação:** arquivos públicos de divulgação de resultados do Tribunal Superior Eleitoral (TSE), totalização por município e zona, 1º turno (eleição 6257) e 2º turno (eleição 6258), lidos em 26/10/2026. A página reflete o estado dos arquivos nessa data; confira com os resultados oficiais em <https://resultados.tse.jus.br/>.
- **Malhas municipais:** IBGE, via [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br) (CC0), simplificadas por este projeto.
- **Malha das UFs e centroides:** API de malhas do IBGE (`servicodados.ibge.gov.br`), simplificadas.

## Limitações

- As malhas foram simplificadas para a página ficar leve (tolerância de 0,008°, grade de 0,004°). A área de cada município difere da original em no máximo 10%; use outra fonte para medir áreas ou fronteiras.
- 7 municípios criados recentemente não têm polígono na malha usada e aparecem como pontos; um município de Mato Grosso aparece apenas na lista.
- O exterior (186 localidades) não tem mapa; aparece em tabelas e nos totais.
- As matrizes de migração usam inferência ecológica (agregados por zona). Elas não observam eleitores individuais, dependem de hipóteses de homogeneidade e têm mais incerteza do que as faixas mostradas, que só refletem a variação entre amostras de municípios. A linha de brancos e nulos é a menos precisa.
- Não há zonas eleitorais georreferenciadas públicas; o desenho por blocos não indica localização.

## Neutralidade e dados pessoais

Painel descritivo e não partidário, sobre uma eleição já encerrada. Usa apenas totais oficiais agregados por zona eleitoral; não contém dados pessoais, não faz projeções nem recomendações e não é um produto do TSE ou do IBGE. A página não usa cookies; a única requisição externa é a contagem anônima de visitas do GoatCounter (mapa-dois-turnos-2026.goatcounter.com), sem dados pessoais.

## Como citar

Use o DOI do Zenodo (badge acima) e o arquivo `CITATION.cff`:

> Coimbra, Paulo C. (2026). *Mapa dos Dois Turnos 2026: votação presidencial por região, estado, município e zona eleitoral* (versão 1.0.0) [Software e dados]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

## Licenças

- Código (`src/`, `tests/`): MIT.
- Dados derivados, textos e `index.html`: CC BY 4.0.
- Dados de origem: TSE (acesso público) e IBGE; malhas municipais de origem em CC0. Detalhes em `LICENSE`.

## Autoria

Paulo C. Coimbra, Departamento de Economia e Finanças, Universidade Federal de Juiz de Fora (UFJF).
