# Publicar no GitHub e gerar o DOI no Zenodo

## 1. Criar o repositório

- Nome: `mapa-dois-turnos-2026`; visibilidade pública (a integração do Zenodo só arquiva repositórios públicos).
- Descrição: *Mapa interativo dos dois turnos da eleição presidencial de 2026 por região, estado, município e zona eleitoral, com dados do TSE, malhas do IBGE e estimativas de migração de votos (inferência ecológica).*
- Site (homepage): `https://pauloccoimbra.github.io/mapa-dois-turnos-2026/`
- Tópicos: `eleicoes-2026`, `eleicoes-brasil`, `segundo-turno`, `tse`, `dados-abertos`, `zonas-eleitorais`, `mapa-interativo`, `visualizacao-de-dados`, `inferencia-ecologica`, `ciencia-politica`, `brasil`, `geojson`, `javascript`, `python`, `github-pages`, `zenodo`, `open-data`, `brazil`, `election-data`, `data-visualization`
- Envie todo o conteúdo da pasta (incluindo `.zenodo.json`, `.gitignore` e `CITATION.cff`, que começam com ponto ou são ocultos no seletor de arquivos; pelo navegador, arraste a pasta inteira ou use o terminal com `git add -A`).

## 2. Ligar o GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`. A página abre em `https://pauloccoimbra.github.io/mapa-dois-turnos-2026/`.

## 3. Ligar o repositório ao Zenodo (antes de criar a release)

1. Entre em <https://zenodo.org> com a conta do GitHub.
2. Menu da conta → *GitHub* (<https://zenodo.org/account/settings/github/>) → *Sync now*.
3. Ligue a chave ao lado de `mapa-dois-turnos-2026`.

## 4. Criar a release

No GitHub: *Releases* → *Draft a new release* → tag `v1.0.0` → título "Mapa dos Dois Turnos 2026 v1.0.0" → *Publish release*. Em alguns minutos o Zenodo cria o registro, lendo os metadados do `.zenodo.json` (o `CITATION.cff` é lido pelo GitHub para o botão "Cite this repository").

## 5. Depois que o DOI sair

O Zenodo gera dois DOIs: o da versão (`10.5281/zenodo.NNNNNNN`) e o DOI "conceito", que sempre aponta para a última versão. Para citar o projeto em geral use o DOI conceito.

1. Troque `XXXXXXX` no `README.md` (badge e citação) e descomente `doi:` no `CITATION.cff`.
2. Preencha seu ORCID no `CITATION.cff` e no registro do Zenodo, se quiser.
3. Publique a correção como `v1.0.1` (uma nova release gera nova versão, sob o mesmo DOI conceito).

## 6. Conferências antes de publicar

- Abra `index.html` localmente e confira os totais nacionais com o resultado oficial do TSE (Lula 64.256.232; Flávio Bolsonaro 59.826.041 no 2º turno).
- Confirme no portal do TSE se os arquivos usados estão na totalização final; se mudarem, regenere a base e recompile (`README.md`, seção "Como reproduzir").
- Escolha de licença: o registro do Zenodo usa CC BY 4.0 (dados e página); o código em `src/` e `tests/` é MIT, conforme o arquivo `LICENSE`. Se preferir uma única licença, altere `LICENSE`, `.zenodo.json` e `CITATION.cff` juntos.
