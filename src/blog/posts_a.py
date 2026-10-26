from base import *
R=S['reg']; U=S['uf']
# ---------------- Post 1: a conta da virada
def p1():
    parts=[('Votos dos outros\ncandidatos',A['outros'],GRY,''),]
    st=stackbar([('Outros candidatos',A['outros'],GRY,Mn(A['outros'])+' mi'),('Comparecimento maior',A['dComp'],BLU,Mn(A['dComp'])+' mi'),('Menos brancos e nulos',A['dBN'],'#7f9bd0',Mn(A['dBN'])+' mi')],
        'Origem dos '+Mn(A['novos'],1)+' milhões de votos que os finalistas ganharam do 1º para o 2º turno',total_lab='Origem dos '+Mn(A['novos'],1)+' milhões de votos novos dos finalistas')
    st2=stackbar([('Lula',A['dL'],LULA,Mn(A['dL'])+' mi  ('+P(A['shareL']*100)+')'),('Flávio Bolsonaro',A['dF'],FLA,Mn(A['dF'])+' mi  ('+P(100-A['shareL']*100)+')')],
        'Divisão dos votos novos entre os finalistas',total_lab='Quem recebeu os '+Mn(A['novos'],1)+' milhões de votos novos')
    rows=sorted(((k,v['shareL']*100) for k,v in R.items()),key=lambda t:-t[1])
    hb=hbars([(k,v) for k,v in rows],'Parcela dos votos novos dos finalistas que foi para Lula, por região',100,[0,25,50,75,100],'% dos votos novos',fmt=lambda v:nb(v,1)+'%',ref=A['shareL']*100,reflab='Brasil '+nb(A['shareL']*100,1)+'%',right=60)
    n=R['Norte']
    tab=table(['','1º turno','2º turno','Variação'],[
        ['Flávio Bolsonaro',f"{N(T['F1'])} ({P(A['F1p'])})",f"{N(T['F2'])} ({P(A['F2p'])})",'+'+N(A['dF'])],
        ['Lula',f"{N(T['L1'])} ({P(A['L1p'])})",f"{N(T['L2'])} ({P(A['L2p'])})",'+'+N(A['dL'])],
        ['Outros candidatos',f"{N(T['O1'])} ({P(A['O1p'])})",'—','—'],
        ['Comparecimento',f"{N(T['r1_comp'])} ({P(A['t1'])})",f"{N(T['r2_comp'])} ({P(A['t2'])})",'+'+N(A['dComp'])],
        ['Brancos + nulos',f"{N(T['BN1'])}",f"{N(T['BN2'])}",'−'+N(A['dBN'])]],cap='Totais nacionais (percentuais: votos válidos; para comparecimento, o eleitorado apto).',small=True)
    body=(p(f"No primeiro turno de 2026, Flávio Bolsonaro teve {P(A['F1p'])} dos votos válidos e Lula {P(A['L1p'])}; os outros candidatos somaram {P(A['O1p'])}, ou {M(A['outros'])} de votos. No segundo turno, Lula chegou a {P(A['L2p'])} e Flávio a {P(A['F2p'])}. A vantagem de {M(A['net1'])} de votos para Flávio virou uma vantagem de {M(A['net2'])} para Lula: uma oscilação líquida de {M(A['swing'])} de votos.")
     +p("Este post faz a conta dessa oscilação com os totais por zona eleitoral. Os registros das urnas dizem onde e quanto os votos mudaram. Não dizem por quê, e nada aqui explica as razões de ninguém.")
     +tab
     +h2('Uma identidade que fecha')
     +p(f"Os dois finalistas somaram {M(T['F1']+T['L1'])} de votos no primeiro turno e {M(T['F2']+T['L2'])} no segundo. A diferença, {M(A['novos'])}, tem três parcelas, e elas somam exatamente esse valor. A primeira são os votos dos outros candidatos no primeiro turno ({Mn(A['outros'])} milhões), que ficaram sem opção própria. A segunda é o aumento do comparecimento ({Mn(A['dComp'])} milhões a mais de pessoas nas urnas). A terceira é a queda de votos brancos e nulos ({Mn(A['dBN'])} milhões a menos, de {Mn(T['BN1'])} para {Mn(T['BN2'])}).")
     +fig(st,'As três parcelas somam a diferença entre o total dos finalistas no 2º turno e no 1º. A identidade vale por construção, porque voto válido é comparecimento menos brancos e nulos.')
     +p("A conta dá o tamanho da bolsa de votos que estava disponível, mas não o caminho de cada voto. Um eleitor de outro candidato pode ter anulado o voto, e um abstêmio do primeiro turno pode ter ocupado o lugar de um eleitor de finalista que desistiu de ir votar. Só se observa o saldo.")
     +h2('Quanto ficou com cada lado')
     +p(f"Dos {M(A['novos'],1)}, {M(A['dL'])} ({P(A['shareL']*100)}) foram líquidos para Lula e {M(A['dF'])} ({P(100-A['shareL']*100)}) para Flávio. A palavra líquido importa: se houve eleitores que trocaram de finalista nos dois sentidos, o saldo esconde essas trocas. O quinto post da série tenta estimá-las.")
     +fig(st2,'Ganho líquido de cada finalista entre os turnos, em milhões de votos e em % do total ganho pelos dois.')
     +h2('A mesma conta por região')
     +p(f"A divisão varia bastante. No Norte, Lula ficou com {P(n['shareL']*100)} dos votos novos dos finalistas ({Mn(n['dL'])} milhão a mais para ele, {nb(n['dF']/1e3,0)} mil a mais para Flávio), numa região em que o comparecimento caiu {nb(abs(n['t2']-n['t1']),1)} ponto percentual. No Nordeste a fatia foi de {P(R['Nordeste']['shareL']*100)}. No Sudeste ficou perto da média nacional ({P(R['Sudeste']['shareL']*100)}), e no Sul e no Centro-Oeste Flávio também recebeu muitos votos novos: Lula ficou com {P(R['Sul']['shareL']*100)} e {P(R['Centro-Oeste']['shareL']*100)}.")
     +fig(hb,'Parcela dos votos novos dos finalistas (diferença entre os votos de cada um no 2º e no 1º turno) que coube a Lula. A linha tracejada é a média nacional.')
     +p(f"A parcela não equivale ao deslocamento da margem em pontos percentuais. O Sudeste, com uma fatia próxima da média, teve o maior deslocamento de margem entre as regiões ({pp(R['Sudeste']['dm'])}, contra {pp(R['Nordeste']['dm'])} no Nordeste). O próximo post mostra que esse deslocamento, medido em pontos, foi muito parecido de uma zona para outra.")
     )
    return post(body)
reg(1,'a-conta-da-virada',f"A conta da virada: de onde vieram os {Mn(A['novos'],1)} milhões de votos novos dos finalistas",
    f"De onde vieram os {Mn(A['novos'],1)} milhões de votos novos de Lula e Flávio Bolsonaro entre os turnos de 2026, nos registros das urnas por zona.",
    ['eleições 2026','segundo turno','dados abertos','TSE'],p1)

# ---------------- Post 2: deslocamento uniforme
def p2():
    z=S['z']; q=z['dm_q']; h=S['dmhist']
    hs=hist(h['edges'],h['share'],'Distribuição do deslocamento da margem por zona',xlabel='mudança da margem Flávio − Lula entre os turnos, em p.p. (negativo = a favor de Lula)')
    fb=S['flipbin']; lab=[f"{b['lo']}–{b['hi']}" if b['hi']<100 else f"{b['lo']}+" for b in fb]
    vb=vbars([b['share'] for b in fb],lab,'Parcela de zonas em que Lula ganhou o 2º turno, por margem de Flávio no 1º turno',ylab='% das zonas virou para Lula',ymax=100,colors=[LULA]*7,xlabel='margem de Flávio sobre Lula no 1º turno (p.p.), faixas',yticks=[0,25,50,75,100],h=270)
    ml={m['modelo']:m for m in S['uniforme']}
    tab=table(['Modelo','RMSE','Erro médio','Viram (prev.)','Acertos','Sinal certo'],
       [[m['modelo'][0].upper()+m['modelo'][1:],pp(m['rmse'],1,False),pp(m['mae'],1,False),N(m['flips']) if m['modelo']!='nenhuma mudança' else '0',N(m['hit']) if m['modelo']!='nenhuma mudança' else '0',P(m['sign'])] for m in S['uniforme']],
       cap='Zonas no Brasil (sem exterior), pesos pelos votos válidos do 2º turno. “Viram” = Flávio à frente no 1º turno e Lula no 2º.',small=True)
    body=(p(f"A mudança da margem entre Flávio e Lula, no Brasil, foi de {pp(A['dm'])} (de {pp(A['m1'])} para {pp(A['m2'])}, sempre Flávio menos Lula, sobre os votos válidos). O número nacional pode ser a média de movimentos muito diferentes ou a repetição de um mesmo movimento em todo lugar. Os registros por zona permitem ver qual dos dois casos é o real.")
     +p(f"Em {P(z['toL'])} das {N(z['n'])} zonas do país (sem o exterior) a margem andou a favor de Lula, o que corresponde a {P(z['toL_w'])} dos votos válidos do segundo turno. A mediana do deslocamento, ponderada pelos votos, é de {pp(q[2],1)}; a metade central das zonas fica entre {nb(q[1],1)} e {nb(q[3],1)}, e 90% delas entre {nb(q[0],1)} e {nb(q[4],1)} p.p. As margens em si variam muito mais: o desvio-padrão da margem do segundo turno entre zonas é de {pp(S['sd_m2'],1,False)}.")
     +fig(hs,'Cada barra reúne as zonas cujo deslocamento caiu na faixa de 1 p.p., pesadas pelos votos válidos do 2º turno. Quase toda a massa está à esquerda do zero.')
     +h2('Um teste simples')
     +p(f"Se o movimento foi aproximadamente o mesmo em toda parte, bastaria somar o deslocamento nacional ({pp(A['dm'])}) à margem de cada zona no primeiro turno para prever o segundo. O resultado é melhor do que se poderia esperar. O erro típico dessa previsão é de {pp(ml['deslocamento nacional único']['rmse'],1,False)}; sem nenhuma mudança, seria de {pp(ml['nenhuma mudança']['rmse'],1,False)}. Dar a cada região o seu próprio deslocamento reduz o erro a {pp(ml['deslocamento por região']['rmse'],1,False)}, e cada UF a {pp(ml['deslocamento por UF']['rmse'],1,False)}. Com o deslocamento observado em cada município, o erro cai a {pp(ml['deslocamento por município']['rmse'],1,False)}.")
     +tab
     +p(f"O deslocamento único também reproduz quem virou. Ele aponta {N(ml['deslocamento nacional único']['flips'])} zonas passando de Flávio para Lula; na realidade foram {N(z['FL'])}, e {N(ml['deslocamento nacional único']['hit'])} delas coincidem. Entre os estados, o único em que a soma do deslocamento nacional atravessa o zero é Minas Gerais, justamente o único que trocou de líder.")
     +h2('Quem virou depende de onde a margem estava')
     +p(f"Como o deslocamento foi parecido, a chance de uma zona virar dependeu quase só de a vantagem de Flávio no primeiro turno ser menor ou maior que esse deslocamento. Entre as zonas em que Flávio liderou por até 2 pontos, todas passaram para Lula; entre 2 e 4 pontos, {P(fb[1]['share'],0)}; entre 4 e 6, {P(fb[2]['share'],0)}; entre 6 e 8, {P(fb[3]['share'],0)}. Nenhuma zona com vantagem de Flávio acima de 8 pontos virou.")
     +fig(vb,f"Número de zonas por faixa: {', '.join(N(b['n']) for b in fb)}. Em cada faixa, a barra mostra quantas passaram a ter Lula à frente no 2º turno.")
     +box("O que isso permite dizer. A virada, vista pelas zonas, foi menos uma mudança na geografia do voto e mais um deslocamento de cerca de cinco pontos e meio na margem, que atingiu quase todos os lugares. Onde Flávio tinha uma vantagem curta, o deslocamento bastou para trocar o líder. A pergunta sobre as causas, portanto, aponta para algo que atuou em todo o país com intensidade parecida, e não para episódios locais. O que se moveu, em votos, é o assunto dos posts 1 e 5.")
     +p(f"O resultado tem um limite claro. Um deslocamento uniforme descreve o padrão, mas não o produz. E o erro não é ruído: ele cai a menos da metade quando se usa o deslocamento de cada município, o que indica diferenças locais sistemáticas. Os posts 3, 4 e 7 olham para elas.")
     )
    return post(body)
reg(2,'a-virada-foi-um-deslocamento-uniforme',f"A virada foi quase um deslocamento uniforme de {nb(abs(A['dm']),1)} pontos",
    f"Em {P(S['z']['toL'],0)} das zonas eleitorais a margem andou a favor de Lula entre os turnos; um deslocamento único prevê o 2º turno com erro de 2 pontos.",
    ['eleições 2026','segundo turno','zonas eleitorais','dados abertos'],p2)
