from base import *
V=S['var']; Z=S['z']; PV=S['pivot']
CT={c['nome']:c for c in S['cities']}
# ---------------- Post 7: dentro dos municípios
def p7():
    names=['SÃO PAULO','RIO DE JANEIRO','BRASÍLIA','BELO HORIZONTE','SALVADOR','FORTALEZA','MANAUS','CURITIBA']
    rows=[(tc(n)+f" ({CT[n]['nz']})",[(zz[2],zz[3]) for zz in CT[n]['zones']],CT[n]['m2']) for n in names]
    st=strip(rows,'Margem Flávio − Lula no 2º turno em cada zona das oito maiores cidades')
    vt=table(['Margem Flávio − Lula','Entre UFs','Entre municípios da mesma UF','Entre zonas do mesmo município'],
        [['No 1º turno',P(V['m1']['uf'],0),P(V['m1']['mun'],0),P(V['m1']['zona'],0)],['No 2º turno',P(V['m2']['uf'],0),P(V['m2']['mun'],0),P(V['m2']['zona'],0)],['Mudança entre os turnos',P(V['dm']['uf'],0),P(V['dm']['mun'],0),P(V['dm']['zona'],0)]],
        cap='Parcela da variância da margem (e da mudança), ponderada pelos votos válidos do 2º turno, que cada nível explica.',small=True)
    def lz(n): return sum(1 for zz in CT[n]['zones'] if zz[2]<0)
    ct=table(['Município','Zonas','Lula à frente','Margem nas zonas (mín. a máx.)','Viraram','Margem do município'],
       [[tc(n)+' ('+CT[n]['uf'].upper()+')',N(CT[n]['nz']),N(lz(n)),f"{nb(CT[n]['zmin'],1,True)} a {nb(CT[n]['zmax'],1,True)}",N(CT[n]['nFL']),pp(CT[n]['m2'])] for n in names],
       cap='Margem Flávio − Lula no 2º turno (p.p.). Zonas que viraram: Flávio à frente no 1º turno e Lula no 2º.',small=True)
    sp=CT['SÃO PAULO']; rj=CT['RIO DE JANEIRO']; bh=CT['BELO HORIZONTE']
    spz=sorted(sp['zones'],key=lambda t:t[2]); 
    body=(p(f"Uma zona eleitoral é um conjunto de seções de votação, agrupadas pela Justiça Eleitoral, e o resultado de cada uma é público. Isso permite olhar dentro dos municípios, o que as estatísticas por cidade escondem. A pergunta deste post é quanto de informação as zonas acrescentam, e onde.")
     +h2('Pouco sobre o nível, mais sobre a mudança')
     +p(f"Medindo a variação da margem Flávio − Lula entre as {N(Z['n'])} zonas do país, {P(V['m2']['uf'],0)} dela é diferença entre UFs, {P(V['m2']['mun'],0)} é diferença entre municípios da mesma UF e só {P(V['m2']['zona'],0)} é diferença entre zonas do mesmo município. Quem conhece o município de uma zona já sabe quase tudo sobre a margem dela no segundo turno. Para a mudança entre os turnos a divisão muda: {P(V['dm']['uf'],0)} entre UFs, {P(V['dm']['mun'],0)} entre municípios e {P(V['dm']['zona'],0)} entre zonas. O deslocamento tem uma componente local, a uma escala menor do que a do município, que a margem em si não tem.")
     +vt
     +h2('Grandes cidades: zonas de lados diferentes')
     +p(f"A parcela de 3% é pequena em termos relativos e grande em termos de pessoas, porque as zonas das grandes cidades são enormes. Em São Paulo, a margem no segundo turno vai de {pp(sp['zmin'],1)} (Lula à frente, na zona {spz[0][0]}) a {pp(sp['zmax'],1)} (Flávio à frente, na zona {spz[-1][0]}), e {lz('SÃO PAULO')} das {sp['nz']} zonas têm Lula na frente. No Rio de Janeiro a amplitude vai de {pp(rj['zmin'],1)} a {pp(rj['zmax'],1)}; das {rj['nz']} zonas, {rj['nFL']} passaram de Flávio para Lula. Em Belo Horizonte, que como município foi para Flávio por {pp(bh['m2'],1,False)}, as {bh['nz']} zonas se distribuem de {pp(bh['zmin'],1)} a {pp(bh['zmax'],1)}, e {bh['nFL']} delas mudaram de lado.")
     +fig(st,'Cada círculo é uma zona (tamanho proporcional ao eleitorado, até 250 mil); o losango é o município. O número de zonas está entre parênteses. Margem negativa: Lula à frente.')
     +ct
     +h2('Onde a eleição ficou apertada')
     +p(f"Uma forma de ler as zonas é procurar as de decisão apertada. São {N(PV['n'])} as zonas em que a margem do segundo turno ficou a menos de 2 pontos de empate, para qualquer lado: juntas, têm {Mn(PV['E'],1)} milhões de eleitores e {P(PV['share'],1)} dos votos válidos do segundo turno. O saldo líquido a favor de Lula, por sua vez, é concentrado: {N(Z['half_swing_zones'])} zonas, {P(Z['half_swing_zones']/Z['n']*100,1)} do total, bastam para somar metade dele.")
     +p(f"Na página do mapa, o município aberto mostra suas zonas como blocos proporcionais ao eleitorado, coloridos pela métrica escolhida. O arranjo é um esquema: as zonas não têm limites geográficos públicos, e a posição dos blocos não indica onde ficam na cidade.")
     +box("Ressalva. A zona eleitoral é uma divisão administrativa da Justiça Eleitoral, e seus limites não coincidem necessariamente com bairros. Comparar zonas de um mesmo município descreve os eleitores que votam em cada uma, e não os moradores de uma região da cidade.")
     )
    return post(body)
reg(7,'dentro-dos-municipios-as-zonas',"Dentro dos municípios: o que as zonas eleitorais mostram sobre a virada",
    'As zonas explicam pouco do nível da margem e mais da sua mudança; São Paulo, Rio e Belo Horizonte têm zonas de lados opostos.',
    ['eleições 2026','zonas eleitorais','municípios','segundo turno'],p7)

# ---------------- Post 8: método
def p8():
    body=(p("As estimativas do post 5 vêm de um modelo estatístico, e a confiança que elas merecem depende de entender o que ele faz e o que não consegue fazer. Este texto reúne o método, a verificação e as limitações. O código e os dados estão no repositório do projeto, e a descrição completa está em docs/METODOLOGIA.md.")
     +h2('O problema')
     +p(f"Não se observa o voto de cada eleitor, só quantos votos cada candidato teve em cada zona, nos dois turnos. A matriz que diz que proporção de cada origem do primeiro turno foi para cada destino do segundo turno é, portanto, uma incógnita. Com as {N(Z['n'])} zonas do país (mais 186 localidades no exterior) e 5 origens e 4 destinos, o modelo tenta achar a matriz que melhor reproduz os totais do segundo turno a partir dos do primeiro. Os destinos são Lula, Flávio, branco ou nulo e abstenção, e as origens, além desses, os outros candidatos reunidos.")
     +h2('Como é estimado')
     +p("O ajuste é de mínimos quadrados ponderados pelo tamanho do eleitorado da zona, com duas restrições: nenhuma taxa pode ser negativa e as taxas de cada origem somam 100%. Para reduzir o ruído, usa-se uma estrutura hierárquica: uma matriz nacional, uma matriz por região que parte da nacional, e uma matriz por UF que parte da regional (a influência da matriz de nível superior é fixada, e as zonas da unidade a corrigem). A abstenção do segundo turno é medida sobre o eleitorado do primeiro, o que preserva a contabilidade entre os turnos. Os intervalos de 95% vêm de um bootstrap que reamostra municípios dentro de cada região (150 réplicas para o Brasil e 100 para regiões e UFs).")
     +h2('Verificação')
     +p("O estimador foi testado em dados simulados. Foram geradas respostas do segundo turno a partir das composições reais do primeiro, com uma matriz verdadeira conhecida e ruído multinomial. Sem heterogeneidade entre regiões, a matriz foi recuperada com erro inferior a 0,1 ponto percentual. Com heterogeneidade (deslocamentos regionais de até 5 pontos nas taxas dos outros candidatos e de até 10 pontos nas dos brancos e nulos), as linhas dos finalistas, dos outros candidatos e da abstenção ficaram a no máximo cerca de 3 pontos da verdade, e a linha dos brancos e nulos a cerca de 11 pontos. É por isso que ela é tratada como a menos confiável.")
     +h2('Limites que nenhum bootstrap corrige')
     +p("Primeiro, a falácia ecológica: o modelo supõe que, dentro de cada unidade, a taxa de transição não depende sistematicamente da composição da zona. Se eleitores de um mesmo candidato se comportam de modo diferente em zonas diferentes por razões que também afetam a composição, a estimativa tem viés. Segundo, só se identificam fluxos líquidos: um eleitor que trocou de candidato e outro que trocou no sentido oposto se anulam. Terceiro, os limites determinísticos de Duncan e Davis, calculados só com os totais, são muito mais largos do que as faixas do modelo. Para o fluxo de eleitores de Flávio para Lula, vão de 0 a 80%. O modelo estreita esse intervalo à custa de hipóteses, e o bootstrap não mede o risco dessas hipóteses.")
     +p("Quarto, as faixas informadas medem a variação entre amostras de municípios, e não a incerteza de especificação. Um quinto limite é prático: os arquivos do TSE foram lidos em 26/10/2026, e atualizações posteriores podem alterar os números em pequena medida. Por fim, as zonas eleitorais não têm malha geográfica pública, e os blocos do mapa são um esquema.")
     +h2('Reprodução')
     +p("A base por zona, as tabelas derivadas, o código do modelo e o código que gera a página estão no repositório. Os totais exibidos pela página foram comparados com as tabelas para as 27 UFs e para todos os municípios, sem divergência. Quem quiser reproduzir os números deste post pode rodar run_desc.py (descritivas), run_est.py e run_uf.py (bootstraps) e validate_sim.py (simulação), nessa ordem, e o script estudos.py da série para as tabelas dos posts 1 a 7.")
     )
    return post(body)
reg(8,'como-ler-as-estimativas',"Como ler as estimativas de migração de votos: o que a inferência ecológica garante e o que não garante",
    'Método, verificação por simulação e limites das estimativas de migração de votos entre os turnos de 2026.',
    ['eleições 2026','inferência ecológica','metodologia','dados abertos'],p8)

# ---------------- Post 0: guia
def p0():
    fl=S['mun']; z=S['z']
    body=(p(f"No segundo turno de 2026, Lula teve {P(A['L2p'])} dos votos válidos e Flávio Bolsonaro {P(A['F2p'])}. No primeiro, Flávio tinha ficado à frente, com {P(A['F1p'])} contra {P(A['L1p'])}. Esta série usa os registros das urnas por zona eleitoral, dos dois turnos, para descrever como a vantagem mudou de lado: de onde vieram os votos, onde a mudança pesou, que parte dela se vê nas zonas, e o que se pode e o que não se pode afirmar. Todos os números saem de uma base pública do TSE e podem ser conferidos no mapa interativo e no repositório do projeto.")
     +p("Os registros das urnas respondem a perguntas sobre onde e quanto. Perguntas sobre por quê, que exigiriam pesquisas com eleitores individuais, ficam fora do alcance e fora do que a série afirma.")
     +h2('Os sete posts')
     +'<ol style="margin:0 0 14px 20px;padding:0;line-height:1.7">'
     +''.join(f'<li style="margin-bottom:8px"><b>{ti}</b> {de}</li>' for ti,de in [
      ('A conta da virada.',f"Os finalistas ganharam {Mn(A['novos'],1)} milhões de votos entre os turnos, e {P(A['shareL']*100,0)} deles foram líquidos para Lula."),
      ('Um deslocamento quase uniforme.',f"Em {P(z['toL'],0)} das zonas a margem andou a favor de Lula, cerca de {nb(abs(A['dm']),1)} pontos em média; esse número prevê o resultado das zonas com erro típico de 2 pontos."),
      ('Onde a virada pesou.',f"Sudeste e Nordeste deram {P((R_['Sudeste']['shareSwing']+R_['Nordeste']['shareSwing'])*100,0)} do saldo; Minas Gerais foi o único estado a trocar de lado."),
      ('Cidades grandes e pequenas.',"O deslocamento cresce com o tamanho do município; o Rio de Janeiro e Macapá foram as capitais que viraram."),
      ('Para onde foram os votos.',"Estimativas de migração: quase nenhuma troca direta entre finalistas; os eleitores dos outros candidatos se dividiram quase ao meio entre os dois, com uma parcela em branco ou nulo."),
      ('Comparecimento, brancos e nulos.',"Mais gente votou, menos gente anulou, e a queda de brancos e nulos acompanhou o deslocamento."),
      ('Dentro dos municípios.',"As zonas acrescentam pouco ao nível da margem e mais à sua mudança; zonas de lados opostos convivem nas grandes cidades.")])
     +'</ol>'
     +p("Um oitavo texto, sobre método e limites das estimativas, complementa a série.")
     +box("Antes de ler: os dados foram lidos em 26/10/2026 nos arquivos de divulgação do TSE. Se houver atualização da totalização, os números podem mudar de modo marginal. A série é descritiva, não partidária, e usa apenas totais oficiais agregados por zona eleitoral, sem dados pessoais.")
     )
    return post(body)
R_=S['reg']
reg(0,'guia-da-serie',"A virada de 2026 nos registros das urnas: guia da série",
    'Série sobre como a vantagem entre Flávio Bolsonaro e Lula mudou de lado entre os turnos de 2026, nos registros das urnas por zona.',
    ['eleições 2026','segundo turno','dados abertos','série'],p0)
