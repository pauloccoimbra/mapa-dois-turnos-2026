from base import *
R=S['reg']; U=S['uf']; Z=S['z']; F=S['flow']
CO=F['col']; DE=F['det']
def pr(x): return nb(x*100,1)+'%'
def ci(r,l,h): return f"{nb(r*100,1)}% <span style='color:#5b6978'>({nb(l*100,1)}–{nb(h*100,1)})</span>"
# ---------------- Post 5: fluxos
def p5():
    O=['Eleitores de Flávio','Eleitores de Lula','Outros candidatos','Brancos e nulos','Abstenção']
    base=[sum(CO['flows'][i]) for i in range(5)]
    rows=[(O[i],[x*100 for x in CO['rates'][i]]) for i in range(5)]
    cols=[('Lula',LULA),('Flávio',FLA),('Branco/nulo',BLU),('Abstenção',LGR)]
    chart=stack100(rows,cols,'Destino estimado no 2º turno dos eleitores de cada origem do 1º turno',left=150)
    tab=table(['Origem no 1º turno','Base (mi)','→ Lula','→ Flávio','→ Branco/nulo','→ Abstenção'],
        [[O[i],Mn(base[i]),*[ci(CO['rates'][i][k],CO['rates_lo'][i][k],CO['rates_hi'][i][k]) for k in range(4)]] for i in range(5)],cap='Taxas de destino estimadas (%), com intervalo de 95% por bootstrap de municípios. Linhas somam 100%.',small=True)
    fl=CO['flows']; lul=[fl[i][0] for i in range(5)]; fla=[fl[i][1] for i in range(5)]
    sl=sum(lul); sf=sum(fla); nm=['Já votavam no finalista','Eleitores do outro finalista','Outros candidatos','Brancos e nulos','Abstenção']
    idx_l=[1,0,2,3,4]; idx_f=[0,1,2,3,4]
    ori=table(['Origem dos votos no 2º turno','Votos de Lula','%','Votos de Flávio','%'],
        [[nm[k],Mn(lul[idx_l[k]],2)+' mi',pr(lul[idx_l[k]]/sl),Mn(fla[idx_f[k]],2)+' mi',pr(fla[idx_f[k]]/sf)] for k in range(5)],cap='Fluxos estimados, em milhões de votos. Os totais diferem em até 0,1 milhão dos votos apurados, por causa do ajuste estatístico.',small=True)
    names=['Caiado','Zema','Cury','Renan Santos']; ix=[2,3,4,5]
    ct=table(['Candidato (1º turno)','Eleitores (mi)','→ Lula','→ Flávio','→ Branco','→ Nulo'],
        [[names[j],Mn(sum(DE['flows'][i]),2),*[ci(DE['rates'][i][k],DE['rates_lo'][i][k],DE['rates_hi'][i][k]) for k in [0,1,2,3]]] for j,i in enumerate(ix)],
        cap='Especificação detalhada (10 origens, 5 destinos). Exploratória: leia como indício. “Abstenção” omitida por ser quase zero nestas linhas.',small=True)
    dd={ (r['origem'],r['destino']):r for r in S['dd']}
    body=(p(f"Os posts anteriores contaram votos: quanto entrou, onde pesou. Falta a pergunta sobre os caminhos. Os registros das urnas não mostram o voto de cada pessoa, só os totais de cada zona, mas esses totais permitem estimar, com um modelo estatístico, a proporção do eleitorado de cada categoria do primeiro turno que foi para cada categoria do segundo. A técnica é conhecida como inferência ecológica e tem limites sérios, descritos no último post da série. Os números abaixo são estimativas, e as faixas informadas só medem a variação entre amostras de municípios.")
     +fig(chart,'Estimativa nacional: para cada origem no 1º turno, como o eleitorado se distribuiu entre as quatro opções do 2º turno. O ajuste usa as 6.292 linhas município × zona (zonas e exterior).')
     +tab
     +h2('O que as estimativas dizem com mais segurança')
     +p(f"Os eleitores de cada finalista ficaram, em sua grande maioria, onde estavam: {pr(CO['rates'][1][0])} dos de Lula votaram nele de novo e {pr(CO['rates'][0][1])} dos de Flávio também. A troca direta entre os finalistas é pequena e assimétrica: {pr(CO['rates'][0][0])} dos eleitores de Flávio teriam passado para Lula (intervalo de {nb(CO['rates_lo'][0][0]*100,1)} a {nb(CO['rates_hi'][0][0]*100,1)}%), e praticamente nenhum no sentido contrário. Em votos, isso dá algo como {Mn(fl[0][0],2)} milhão. Os dados, sozinhos, admitem trocas bem maiores: sem o modelo, só a contabilidade dos totais já é compatível com até {nb(dd[('Flávio','Lula')]['max_%linha'],0)}% dos eleitores de Flávio indo para Lula. O modelo escolhe, entre as possibilidades, a mais plausível dentro de suas hipóteses, e é isso que as faixas refletem.")
     +p(f"Os eleitores dos outros candidatos, {Mn(base[2],2)} milhões, são o grupo mais disputado: {pr(CO['rates'][2][0])} para Lula, {pr(CO['rates'][2][1])} para Flávio e {pr(CO['rates'][2][2])} para branco ou nulo. A diferença entre os dois finalistas, de menos de quatro pontos, é pequena perto da incerteza do modelo. A abstenção do primeiro turno, de {Mn(base[4],1)} milhões de pessoas, teria alimentado sobretudo Lula (estimados {Mn(fl[4][0],2)} milhão de votos, ou {pr(CO['rates'][4][0])}), com {pr(CO['rates'][4][1])} para Flávio.")
     +ori
     +h2('A linha mais frágil')
     +p(f"A estimativa para brancos e nulos é a mais extrema: {pr(CO['rates'][3][0])} teriam votado em Lula no segundo turno. Isso valeria {Mn(fl[3][0],2)} milhões de votos, o maior fluxo individual para ele depois dos que já votavam nele. Nenhuma conclusão deveria se apoiar nesse número. Num teste com dados simulados, em que a matriz verdadeira era conhecida e variava entre regiões, o estimador errou essa linha em cerca de 11 pontos (71% estimado contra 60% verdadeiro), e acertou as demais com erro de até 3 pontos. A linha é difícil por uma razão estrutural: o total de brancos e nulos caiu só {Mn(A['dBN'],2)} milhão entre os turnos, de modo que o fluxo estimado para Lula implica movimentos brutos grandes em sentidos opostos, que os totais por zona não conseguem separar com folga. O que dá para afirmar com mais cautela é que brancos e nulos não parecem ter ido para Flávio em proporção relevante.")
     +h2('Candidato por candidato: um indício')
     +p("Uma versão do modelo separa os quatro principais candidatos do primeiro turno depois dos finalistas. Ela produz números nítidos, e a nitidez engana: eleitorados de candidatos que se concentram nas mesmas zonas são difíceis de distinguir, e cada linha usa menos informação do que a nacional. Trate a tabela como hipótese para estudos futuros, e não como medida.")
     +ct
     +p(f"Os padrões estimados são distintos entre os candidatos: Zema com quase todo o eleitorado indo a Flávio, Renan Santos majoritariamente a Flávio, Caiado dividido entre os dois finalistas com pequena parcela de branco e nulo, e Cury com uma parte importante em voto branco e nulo. Se essas diferenças se confirmarem com dados individuais, como pesquisas de intenção de voto ou estudos com amostras, elas ajudariam a entender por que o grupo dos outros candidatos se dividiu como se dividiu. Com as zonas apenas, não passam de um indício.")
     )
    return post(body)
reg(5,'para-onde-foram-os-votos',"Para onde foram os votos dos outros candidatos, dos brancos e nulos e dos que não votaram",
    'Estimativas de migração de votos entre os turnos de 2026 por inferência ecológica, com intervalos e limites do modelo.',
    ['eleições 2026','segundo turno','inferência ecológica','migração de votos'],p5)

# ---------------- Post 6: comparecimento, brancos e nulos
def p6():
    rg=['Sudeste','Nordeste','Sul','Norte','Centro-Oeste','Exterior']
    tab=table(['Região','Comparec. 1º','Comparec. 2º','Variação','B+N 1º','B+N 2º','Variação'],
       [[r,P(R[r]['t1']),P(R[r]['t2']),pp(R[r]['t2']-R[r]['t1']),P(R[r]['bn1']),P(R[r]['bn2']),pp(R[r]['bn2']-R[r]['bn1'])] for r in rg]+
       [['Brasil',P(A['t1']),P(A['t2']),pp(A['t2']-A['t1']),P(A['bn1']),P(A['bn2']),pp(A['bn2']-A['bn1'])]],
       cap='Comparecimento: % do eleitorado apto do 1º turno (o 2º usa o eleitorado do próprio turno). B+N = brancos + nulos, % dos comparecentes.',small=True)
    q=S['qbn']
    vb=vbars([x['dm'] for x in q],[f"{nb(x['bn1_lo'],1)}–{nb(x['bn1_hi'],1)}%" for x in q],'Deslocamento da margem por quintil de brancos e nulos no 1º turno',ylab='mudança da margem (p.p.)',ymin=-8,ymax=0,fmt=lambda v:nb(v,1),colors=[LULA]*5,xlabel='faixa de brancos + nulos no 1º turno, por quintil de zonas',yticks=[-8,-6,-4,-2,0],h=260)
    cr=S['corr']; dq=S['dt_q']
    body=(p(f"Dois movimentos acompanharam a mudança da margem sem pertencerem a nenhum dos finalistas: mais gente foi às urnas e menos gente votou em branco ou anulou. O comparecimento subiu de {P(A['t1'])} para {P(A['t2'])} do eleitorado ({Mn(A['dComp'],2)} milhões de comparecentes a mais). Os brancos e nulos, que eram {P(A['bn1'])} dos comparecentes, caíram para {P(A['bn2'])}: os brancos de {P(A['br1'])} para {P(A['br2'])}, os nulos de {P(A['nu1'])} para {P(A['nu2'])}.")
     +tab
     +p(f"O comparecimento subiu em {P(Z['tUp'],0)} das zonas, com mediana de {pp(dq[2])} (metade central entre {nb(dq[1],1)} e {nb(dq[3],1)}). A exceção regional é o Norte, onde recuou {nb(abs(R['Norte']['t2']-R['Norte']['t1']),1)} ponto, e onde a margem ainda assim se deslocou {nb(abs(R['Norte']['dm']),1)} pontos. Entre as zonas de um mesmo estado, a associação entre a variação do comparecimento e o deslocamento da margem é fraca, e de sinal negativo (correlação de {nb(cr['dt']['dentro'],2)}): as zonas onde o comparecimento mais subiu foram, em média, um pouco mais para Lula.")
     +h2('Brancos e nulos e o deslocamento')
     +p(f"A relação com brancos e nulos é bem mais forte. Dividindo as zonas em cinco grupos iguais pela taxa de brancos e nulos no primeiro turno, o deslocamento médio da margem cresce de {pp(q[0]['dm'])} no grupo de menor taxa ({nb(q[0]['bn1'],1)}%) para {pp(q[4]['dm'])} no de maior taxa ({nb(q[4]['bn1'],1)}%). Dentro de cada estado, a correlação entre a taxa de brancos e nulos no primeiro turno e o deslocamento é de {nb(cr['bn1']['dentro'],2)}, e a correlação entre a queda dessa taxa e o deslocamento é de {nb(cr['dbn']['dentro'],2)} (positiva, porque a queda é negativa e o deslocamento a favor de Lula também).")
     +fig(vb,'Deslocamento médio da margem Flávio − Lula (p.p., negativo = a favor de Lula) por quintil de zonas, ponderado pelos votos válidos. Cada quintil tem cerca de 1.220 zonas.')
     +p(f"Essa associação aparece sem modelo algum: onde havia proporcionalmente mais brancos e nulos no primeiro turno, a margem andou mais. Ela é compatível com a estimativa do post anterior, que atribui a esses eleitores uma migração forte para Lula, mas não a comprova. Os quintis diferem em muita coisa além da taxa de brancos e nulos; o grupo de maior taxa tinha Lula {pp(abs(q[4]['m1']),1,False)} à frente no primeiro turno, e o de menor taxa Flávio {pp(q[0]['m1'],1,False)} à frente. A correlação dentro de cada UF reduz essa mistura entre regiões, mas não as diferenças entre zonas.")
     +box("O que se pode e o que não se pode dizer. Mais comparecimento e menos votos brancos e nulos acompanharam, no mapa, o deslocamento da margem. Os registros mostram que isso aconteceu nos mesmos lugares. Não mostram se os eleitores que passaram a votar são os mesmos que passaram a escolher um finalista, e a ligação entre os dois fenômenos continua sendo uma hipótese.")
     )
    return post(body)
reg(6,'comparecimento-brancos-e-nulos',"Comparecimento, brancos e nulos: o que mudou entre os dois turnos de 2026",
    'O comparecimento subiu 1,9 ponto, brancos e nulos caíram de 4,8% para 3,2% dos comparecentes, e a queda acompanhou a margem.',
    ['eleições 2026','segundo turno','comparecimento','votos brancos e nulos'],p6)
