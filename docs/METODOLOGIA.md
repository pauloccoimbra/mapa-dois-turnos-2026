# Metodologia

## 1. Dados

Base `dados/zonas_2026_t1_t2.csv`: uma linha por município × zona eleitoral (6.292 linhas: 5.571 municípios e 186 localidades no exterior), com eleitorado apto, comparecimento, brancos, nulos, votos válidos e votos de cada candidato no 1º turno (eleição 6257) e no 2º turno (eleição 6258), a partir dos arquivos públicos de divulgação do TSE lidos em 26/10/2026. O dicionário está em `DICIONARIO_DE_DADOS.md`.

Conferência interna: os totais da página coincidem com as tabelas `dados/derivados/desc_uf.csv` e `desc_mun.csv` para as 27 UFs, o exterior e os 5.757 municípios/localidades (`tests/verificar_totais.py`, tolerância de 0,5 voto).

## 2. Indicadores descritivos

Por zona, município, UF, região e Brasil (`src/analise/run_desc.py`):

- **Participação dos finalistas:** votos de cada finalista sobre os votos válidos de cada turno (no 1º turno a base inclui os demais candidatos).
- **Margem** = % de Flávio Bolsonaro − % de Lula nos votos válidos; positiva indica Flávio à frente. **Mudança da margem** = margem do 2º turno − margem do 1º.
- **Comparecimento** = comparecentes / eleitorado apto do próprio turno. **Brancos e nulos** são medidos como % dos comparecentes.
- **"Virou"**: o líder entre os dois finalistas no 2º turno é diferente do líder no 1º, na unidade.

## 3. Migração de votos (inferência ecológica)

Pergunta: como o eleitorado de cada categoria do 1º turno se distribuiu entre as categorias do 2º? Origem (5): Flávio, Lula, outros candidatos, brancos + nulos, abstenção. Destino (4): Lula, Flávio, brancos + nulos, abstenção. Uma versão detalhada separa Caiado, Zema, Cury, Renan Santos, demais candidatos, brancos e nulos (`fluxos_especificacoes.json`).

Em cada zona *i*, os contagens do 2º turno são modeladas como combinação linear das do 1º, `Y_i ≈ X_i · P`, com `P` uma matriz de transição desconhecida (linhas somam 1, elementos ≥ 0).

- **Estimador:** mínimos quadrados ponderados por 1/E_i (E = eleitorado), com restrições de caixa e de soma 1 por linha, resolvido por SLSQP (`src/analise/lib.py`, `fit_P`).
- **Abstenção do 2º turno** é medida sobre o eleitorado do 1º turno (E1 − comparecentes do 2º), para preservar a identidade contábil entre os turnos.
- **Ajuste hierárquico:** `P` nacional → `P` por região (encolhida ao nacional, κ = 50) → `P` por UF (encolhida à região, κ = 30). Os fluxos de Brasil e regiões agregam os ajustes regionais.
- **Incerteza:** bootstrap por município (reamostra municípios dentro de cada região; 150 réplicas no Brasil e 100 em regiões/UFs, sementes fixas). As faixas são percentis 2,5–97,5% das taxas.
- **Exibição:** a página mostra matrizes apenas para Brasil, regiões e UFs. Abaixo disso há poucas zonas por unidade para estimar transferências com segurança.

### Resultados nacionais (taxas de destino por origem)

| Origem \ Destino | Lula | Flávio | Brancos+nulos | Abstenção |
|---|---|---|---|---|
| Eleitores de Flávio | 0,4% (0,3–0,5) | 98,9% (98,5–99,1) | 0,4% (0,2–0,6) | 0,3% (0,2–0,7) |
| Eleitores de Lula | 99,7% (99,5–99,7) | 0,0% | 0,0% | 0,3% (0,3–0,5) |
| Outros candidatos | 40,3% (38,2–42,0) | 43,9% (41,2–46,8) | 15,7% (13,4–17,8) | 0,1% |
| Brancos e nulos | 80,7% (77,6–83,7) | 0,1% | 19,2% (16,2–22,3) | 0,0% |
| Abstenção | 5,3% (4,6–6,4) | 0,8% (0,5–1,2) | 3,8% (3,0–4,5) | 90,1% (89,0–90,7) |

### Validação por simulação (`src/analise/validate_sim.py`)

Geram-se dados com uma matriz verdadeira conhecida, usando as composições reais do 1º turno e ruído multinomial, com e sem heterogeneidade regional (deslocamentos de ±5 p.p. em "outros → finalistas" e ±10 p.p. em "brancos e nulos → Lula"). Sem heterogeneidade, o estimador recupera a matriz com erro inferior a 0,1 p.p. Com heterogeneidade, as linhas de Flávio, Lula, outros e abstenção ficam a até cerca de 3 p.p. da verdade; a linha de brancos e nulos fica cerca de 11 p.p. acima no destino Lula (71% estimado contra 60% verdadeiro). Por isso essa linha é apontada como a menos precisa.

### O que a inferência ecológica não garante

- Fluxos líquidos: um eleitor que trocou de candidato e outro que trocou no sentido oposto se compensam. Os limites determinísticos de Duncan–Davis (`limites_duncan_davis.csv`) mostram a faixa compatível com os totais, que é bem mais larga do que as estimativas.
- Falácia ecológica: a identificação depende de que as taxas de transição não variem sistematicamente com a composição da zona dentro de cada unidade.
- As faixas de 95% do bootstrap cobrem a variação amostral de municípios e subestimam a incerteza de especificação.

## 4. Mapa

- **Malhas municipais:** GeoJSON do IBGE (via tbrugz/geodata-br, CC0), simplificado com preservação de topologia (`shapely.coverage_simplify`, tolerância 0,008°), coordenadas quantizadas em passos de 0,004° e codificadas por deltas. `src/pagina/simplificar_malhas.py` audita a área de cada município contra a malha de origem e usa um plano B (`simplify` com topologia) quando a diferença passa de 12%. Resultado: 5.564 polígonos, diferença máxima de área de 10%.
- **UFs e centroides:** API de malhas do IBGE. Os 7 municípios sem polígono na malha usada aparecem como pontos nos centroides.
- **Zonas:** não há malha pública das zonas eleitorais. Cada município mostra suas zonas como um *treemap* (área ∝ eleitorado do 2º turno; cor = métrica selecionada), que não tem posição geográfica.
- **Cores:** escala divergente (azul-esverdeado = Lula, âmbar = Flávio) centrada em zero para margens; escala sequencial para comparecimento e brancos + nulos. Os limites das escalas são fixos para cada métrica e nível do mapa.

## 5. Verificação

- `tests/verificar_totais.py`: compara, para cada UF e cada município, os votos exibidos pela página com as tabelas do pipeline.
- `tests/varredura_interface.py`: abre Brasil, regiões, UFs e uma amostra de municípios em todas as métricas, nos temas claro e escuro, buscando valores `NaN`, `undefined` ou `Infinity`, erros de console e blocos de zonas cuja área não some o total.
