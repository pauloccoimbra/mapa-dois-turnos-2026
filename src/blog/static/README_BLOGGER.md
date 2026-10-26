# Série de posts para o Blogger — a virada de 2026 nos registros das urnas

Autor: Paulo C. Coimbra · Blog: pccoimbra.blogspot.com · Dados: TSE (1º e 2º turnos, lidos em 26/10/2026) por município × zona eleitoral.

## Como publicar cada post

1. Blogger → *Nova postagem* → alternar para **Visualização HTML** (ícone `<>`).
2. Colar o conteúdo de `posts/NN-slug.html` (já tem estilos inline e gráficos em SVG, fundo branco).
3. Preencher *Título*, *Marcadores* e *Descrição de pesquisa* (abaixo) e, em *Link permanente*, o slug sugerido.
4. Voltar à Visualização *Redigir* só para conferir; evitar editar nela, pois pode reescrever o HTML.
5. **Plano B se o Blogger remover os SVG:** usar os PNGs de `imagens/` (arquivo `NN-slug-figK.png`, 2x), inserindo-os com *Inserir imagem* no lugar do gráfico, e manter a legenda.
6. `previa.html` mostra a série inteira no navegador antes de publicar.

## Ordem e metadados

| Ordem | Arquivo | Título | Marcadores | Gráficos |
|---|---|---|---|---|
| 0 | `posts/00-guia-da-serie.html` | A virada de 2026 nos registros das urnas: guia da série | eleições 2026, segundo turno, dados abertos, série | 0 |
| 1 | `posts/01-a-conta-da-virada.html` | A conta da virada: de onde vieram os 14,1 milhões de votos novos dos finalistas | eleições 2026, segundo turno, dados abertos, TSE | 3 |
| 2 | `posts/02-a-virada-foi-um-deslocamento-uniforme.html` | A virada foi quase um deslocamento uniforme de 5,4 pontos | eleições 2026, segundo turno, zonas eleitorais, dados abertos | 2 |
| 3 | `posts/03-onde-a-virada-pesou.html` | Onde a virada pesou: Sudeste e Nordeste deram 81% do saldo, e Minas foi o único estado a trocar de lado | eleições 2026, segundo turno, regiões, estados | 1 |
| 4 | `posts/04-capitais-grandes-e-pequenos-municipios.html` | Cidades grandes e pequenas: o deslocamento foi maior onde havia mais eleitores | eleições 2026, segundo turno, capitais, municípios | 1 |
| 5 | `posts/05-para-onde-foram-os-votos.html` | Para onde foram os votos dos outros candidatos, dos brancos e nulos e dos que não votaram | eleições 2026, segundo turno, inferência ecológica, migração de votos | 1 |
| 6 | `posts/06-comparecimento-brancos-e-nulos.html` | Comparecimento, brancos e nulos: o que mudou entre os dois turnos de 2026 | eleições 2026, segundo turno, comparecimento, votos brancos e nulos | 1 |
| 7 | `posts/07-dentro-dos-municipios-as-zonas.html` | Dentro dos municípios: o que as zonas eleitorais mostram sobre a virada | eleições 2026, zonas eleitorais, municípios, segundo turno | 1 |
| 8 | `posts/08-como-ler-as-estimativas.html` | Como ler as estimativas de migração de votos: o que a inferência ecológica garante e o que não garante | eleições 2026, inferência ecológica, metodologia, dados abertos | 0 |

### Descrições de pesquisa (≤ 150 caracteres)

- **0** (130): Série sobre como a vantagem entre Flávio Bolsonaro e Lula mudou de lado entre os turnos de 2026, nos registros das urnas por zona.
- **1** (131): De onde vieram os 14,1 milhões de votos novos de Lula e Flávio Bolsonaro entre os turnos de 2026, nos registros das urnas por zona.
- **2** (136): Em 97% das zonas eleitorais a margem andou a favor de Lula entre os turnos; um deslocamento único prevê o 2º turno com erro de 2 pontos.
- **3** (126): Margens do 1º e do 2º turno de 2026 por região e UF, saldo líquido em votos e o caso de Minas Gerais, nos registros das urnas.
- **4** (114): Margem Flávio − Lula por tamanho de município e nas capitais, nos dois turnos de 2026, e o caso do Rio de Janeiro.
- **5** (118): Estimativas de migração de votos entre os turnos de 2026 por inferência ecológica, com intervalos e limites do modelo.
- **6** (124): O comparecimento subiu 1,9 ponto, brancos e nulos caíram de 4,8% para 3,2% dos comparecentes, e a queda acompanhou a margem.
- **7** (125): As zonas explicam pouco do nível da margem e mais da sua mudança; São Paulo, Rio e Belo Horizonte têm zonas de lados opostos.
- **8** (105): Método, verificação por simulação e limites das estimativas de migração de votos entre os turnos de 2026.

### Links permanentes sugeridos

- `00-guia-da-serie`
- `01-a-conta-da-virada`
- `02-a-virada-foi-um-deslocamento-uniforme`
- `03-onde-a-virada-pesou`
- `04-capitais-grandes-e-pequenos-municipios`
- `05-para-onde-foram-os-votos`
- `06-comparecimento-brancos-e-nulos`
- `07-dentro-dos-municipios-as-zonas`
- `08-como-ler-as-estimativas`

## Post 0 (guia) no formato "Boletim da Apuração"

`posts/00-guia-da-serie.html` segue o mesmo estilo da edição especial do 2º turno (fundo pergaminho, manchete, roteiro de leitura, cartões e rodapé ❀). Os 8 links usam os permalinks sugeridos acima; o Blogger corta os slugs conforme o título, então confira e corrija cada link depois de publicar os posts 1–8. Título sugerido: *Edição especial: a virada de 2026 nos registros das urnas, guia de leitura*.

## Depois de publicar

- Publicar o post 0 (guia) por último ou editá-lo ao final, para inserir os links dos demais posts.
- Cada post termina com rodapé (fontes, URL do mapa, repositório, declaração de neutralidade). Conferir se as URLs do mapa e do repositório estão corretas após subir o repositório no GitHub.
- Quando existir o DOI do Zenodo do repositório, acrescentar a citação no rodapé de cada post (substituir o marcador `10.5281/zenodo.XXXXXXX`, se presente).
- Inserir links cruzados "anterior/próximo" entre os posts.

## Reprodução

Os scripts estão no repositório `mapa-dois-turnos-2026`, em `src/blog/`. `python3 src/blog/estudos.py` recalcula `dados/derivados/estudos_stats.json` (todos os números citados) e `python3 src/blog/gerar.py` reescreve esta pasta `blog/` (requer playwright para os PNGs). O guia (post 0) e este arquivo ficam em `src/blog/static/`.

## Observações editoriais

- Série descritiva e não causal; não atribui motivos a eleitores. Linguagem neutra e sem recomendação de voto.
- Só há totais oficiais agregados por zona; nenhum dado pessoal.
- As estimativas de migração por candidato são exploratórias (inferência ecológica); a linha de brancos e nulos é a mais frágil. O post 8 explica os limites.
