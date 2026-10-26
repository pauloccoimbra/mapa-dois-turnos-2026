from base import *
R=S['reg']; U=S['uf']; Z=S['z']
# ---------------- Post 3: regiões e estados
def p3():
    order=['Sudeste','Nordeste','Sul','Norte','Centro-Oeste']
    tab=table(['Região','Eleitorado','Margem 1º','Margem 2º','Mudança','Saldo líquido p/ Lula','% do saldo'],
      [[r,P(R[r]['elShare']*100),pp(R[r]['m1']),pp(R[r]['m2']),pp(R[r]['dm']),Mn(R[r]['swing'])+' mi',P(R[r]['shareSwing']*100)] for r in order]+
      [['Exterior',P(R['Exterior']['elShare']*100),pp(R['Exterior']['m1']),pp(R['Exterior']['m2']),pp(R['Exterior']['dm']),Mn(R['Exterior']['swing'])+' mi',P(R['Exterior']['shareSwing']*100)]],
      cap='Margem = Flávio − Lula, em % dos votos válidos. “Saldo líquido” é o aumento da vantagem de Lula sobre Flávio, em votos (a oscilação total é de '+Mn(A['swing'])+' milhões).',small=True)
    assert all(v['dm']<0 for v in U.values())
    rows=sorted(((k,v['m1'],v['m2']) for k,v in U.items()),key=lambda t:t[2])
    db=dumbbell(rows,'Margem Flávio − Lula por UF, 1º e 2º turnos',(-60,50),[-50,-25,0,25,50],'margem em p.p.',left=46,highlight=('MG',))
    sw=sorted(U.items(),key=lambda kv:-kv[1]['swing']); top4=sw[:4]; s4=sum(v['swing'] for k,v in top4)/A['swing']*100
    dmo=sorted(U.items(),key=lambda kv:kv[1]['dm'])
    mg=U['MG']; ap=U['AP']; nt=R['Norte']
    body=(p(f"Todas as regiões do país deram a Lula um saldo líquido positivo entre os turnos, mas em tamanhos muito diferentes. O Sudeste respondeu por {P(R['Sudeste']['shareSwing']*100)} da oscilação de {Mn(A['swing'])} milhões de votos na vantagem sobre Flávio, com {P(R['Sudeste']['elShare']*100,0)} do eleitorado. O Nordeste, com {P(R['Nordeste']['elShare']*100,0)} do eleitorado, respondeu por {P(R['Nordeste']['shareSwing']*100)}. Somadas, as duas regiões deram {P((R['Sudeste']['shareSwing']+R['Nordeste']['shareSwing'])*100,0)} do saldo. O Sul, que tem {P(R['Sul']['elShare']*100,0)} do eleitorado, contribuiu com {P(R['Sul']['shareSwing']*100)}.")
     +tab
     +h2('Todos os estados se moveram na mesma direção')
     +p(f"Nos 27 estados, a margem entre Flávio e Lula mudou a favor de Lula. A mudança variou de {pp(dmo[-1][1]['dm'])} em {dmo[-1][0]} a {pp(dmo[0][1]['dm'])} em {dmo[0][0]}. Os maiores deslocamentos foram os de {', '.join(f'{k} ({nb(v['dm'],1)})' for k,v in dmo[:5])}. Os menores, os de {', '.join(f'{k} ({nb(v['dm'],1)})' for k,v in dmo[::-1][:5])}. Nos estados em que Flávio tinha a maior vantagem no primeiro turno a mudança tendeu a ser menor: entre as zonas, a correlação entre a margem inicial e o deslocamento é de {nb(S['corr']['m1']['bruta'],2)}, positiva, ou seja, margens mais favoráveis a Flávio andam com deslocamentos menos intensos.")
     +fig(db,'Cada linha vai da margem do 1º turno (círculo vazado) à do 2º (círculo cheio). Margem negativa: Lula à frente; positiva: Flávio à frente. Estados em ordem da margem do 2º turno. Minas Gerais, em negrito, é o único que muda de lado.')
     +h2('Minas Gerais: o único estado que trocou de líder')
     +p(f"Em Minas, Flávio estava {pp(mg['m1'],1,False)} à frente no primeiro turno e Lula terminou o segundo com {pp(abs(mg['m2']),1,False)} de vantagem: {N(mg['L2'])} votos contra {N(mg['F2'])} para Flávio, uma diferença de {N(mg['L2']-mg['F2'])} votos num estado de {Mn(mg['r2_validos'],1)} milhões de votos válidos. A virada mineira não foi concentrada. Foram {S['mun']['FL_mg']} municípios mineiros em que a liderança passou de Flávio para Lula, o maior número entre os estados, e {Z['FL_by_uf'].get('mg',0)} zonas. O saldo líquido de Minas na oscilação nacional ({Mn(mg['swing'])} milhão) é o segundo entre os estados, atrás de São Paulo.")
     +p(f"Com a mudança, Lula passou a liderar em {S['uf_L2']} estados, contra {S['uf_L1']} no primeiro turno. No Amapá a disputa inicial foi quase um empate: Lula teve {N(ap['L1']-ap['F1'])} votos a mais que Flávio no primeiro turno, em mais de {nb(ap['r1_validos']/1e3,0)} mil votos válidos.")
     +h2('Quatro estados e o Norte como um todo')
     +p(f"{', '.join(f'{k} ({Mn(v['swing'])} mi)' for k,v in top4[:3])} e {top4[3][0]} ({Mn(top4[3][1]['swing'])} mi) somam {P(s4,0)} do saldo líquido nacional. São também os quatro maiores eleitorados do país. O Norte merece uma nota. Como região, passou de uma vantagem de Flávio de {pp(nt['m1'],1,False)} no primeiro turno a um empate quase exato no segundo: Lula ficou à frente por {N(nt['L2']-nt['F2'])} votos em {Mn(nt['r2_validos'],1)} milhões de votos válidos. Ali o comparecimento caiu, de {P(nt['t1'])} para {P(nt['t2'])} do eleitorado, e ainda assim a margem se deslocou {nb(abs(nt['dm']),1)} pontos.")
     +box("Leitura. O tamanho da virada em votos depende de onde estão os eleitores: Sudeste e Nordeste decidiram o saldo. O sentido do movimento, em compensação, foi o mesmo em todos os estados. Quem busca uma explicação precisa dar conta dos dois fatos.")
     )
    return post(body)
reg(3,'onde-a-virada-pesou',f"Onde a virada pesou: Sudeste e Nordeste deram {P((R['Sudeste']['shareSwing']+R['Nordeste']['shareSwing'])*100,0)} do saldo, e Minas foi o único estado a trocar de lado",
    'Margens do 1º e do 2º turno de 2026 por região e UF, saldo líquido em votos e o caso de Minas Gerais, nos registros das urnas.',
    ['eleições 2026','segundo turno','regiões','estados'],p3)

# ---------------- Post 4: tamanho do município e capitais
def p4():
    sz=S['size']; cp=S['cap']; c1=cp['cap']; c2=cp['res']
    tab=table(['Eleitorado do município','Municípios','% do eleitorado','Margem 1º','Margem 2º','Mudança','% do saldo'],
       [[r['cl'],N(r['n']),P(r['elShare']*100),pp(r['m1']),pp(r['m2']),pp(r['dm']),P(r['shareSwing']*100)] for r in sz],
       cap='Municípios do Brasil (sem o exterior) classificados pelo eleitorado apto no 1º turno.',small=True)
    db=dumbbell([(r['cl'],r['m1'],r['m2']) for r in sz],'Margem Flávio − Lula por tamanho de município',(-20,20),[-20,-10,0,10,20],'margem em p.p.',left=118)
    top=cp['tab'][:10]
    tc_=table(['Capital','Eleitorado','Margem 1º','Margem 2º','Mudança'],[[tc(n)+' ('+u.upper()+')',N(e),pp(m1),pp(m2),pp(dm)] for n,u,e,m1,m2,dm in top],cap='As dez maiores capitais (inclui Brasília) por eleitorado.',small=True)
    rio=[c for c in S['cities'] if c['nome']=='RIO DE JANEIRO'][0]
    body=(p(f"A pergunta natural depois de ver que o deslocamento foi geral é se ele foi igual nas cidades grandes e nas pequenas. Não foi, embora a diferença seja de grau. Agrupando os {N(S['mun']['n'])} municípios por tamanho do eleitorado, a margem entre Flávio e Lula se deslocou {pp(sz[0]['dm'],1)} nos municípios com até 5 mil eleitores e {pp(sz[-1]['dm'],1)} nos {sz[-1]['n']} com mais de 500 mil, um gradiente quase contínuo.")
     +tab
     +fig(db,'Margem Flávio − Lula do 1º ao 2º turno por classe de tamanho do município. Lula já liderava no 1º turno nas faixas de 5 a 50 mil eleitores; Flávio, nas menores e nas maiores.')
     +p(f"Os {sz[-1]['n']} maiores municípios, com {P(sz[-1]['elShare']*100,0)} do eleitorado, concentraram {P(sz[-1]['shareSwing']*100,0)} do saldo líquido para Lula, ou {Mn(sz[-1]['swing'])} milhão de votos. Nos municípios de 20 a 50 mil eleitores, o saldo foi de {Mn(sz[3]['swing'])} milhão, a maior soma depois da faixa mais alta. A fatia dos votos novos dos finalistas que foi para Lula, por sua vez, fica entre {P(min(r['shareL'] for r in sz)*100,0)} e {P(max(r['shareL'] for r in sz)*100,0)} em todas as classes. O que muda com o tamanho é a posição inicial da margem e a intensidade do deslocamento, e não a divisão dos votos novos.")
     +h2('As capitais')
     +p(f"As 26 capitais e Brasília reúnem {P(cp['elShare'],1)} do eleitorado e foram {P(cp['swShare'],1)} do saldo líquido. Juntas, passaram de uma margem de {pp(c1['m1'])} no primeiro turno (praticamente empatadas) para {pp(c1['m2'])}. No resto do país a margem foi de {pp(c2['m1'])} para {pp(c2['m2'])}: Flávio à frente no primeiro turno e Lula à frente no segundo, mas com um deslocamento menor ({pp(c2['dm'])}, contra {pp(c1['dm'])} nas capitais).")
     +tc_
     +p(f"Duas capitais trocaram de lado, {tc(cp['FL'][0])} e {tc(cp['FL'][1])}, e Lula passou a liderar em {cp['L2n']} das 27, contra {cp['L1n']} no primeiro turno. A maior delas é o Rio de Janeiro, com {Mn(rio['E'],2)} milhões de eleitores: Flávio liderava por {pp(rio['m1'],1,False)} e perdeu por {pp(abs(rio['m2']),1,False)}, um deslocamento de {pp(rio['dm'])}, o segundo maior entre as dez maiores capitais, depois de Salvador. Das {rio['nz']} zonas do município, {rio['nFL']} passaram de Flávio para Lula. O saldo líquido do Rio foi de {Mn(rio['swing'])} milhão de votos.")
     +box("Uma ressalva de método. O tamanho do eleitorado é um substituto grosseiro de características como urbanização, renda ou escolaridade, que não estão na base de resultados. Os padrões acima descrevem como o deslocamento se distribuiu, e não permitem dizer que o tamanho do município o produziu.")
     )
    return post(body)
reg(4,'capitais-grandes-e-pequenos-municipios',f"Cidades grandes e pequenas: o deslocamento foi maior onde havia mais eleitores",
    'Margem Flávio − Lula por tamanho de município e nas capitais, nos dois turnos de 2026, e o caso do Rio de Janeiro.',
    ['eleições 2026','segundo turno','capitais','municípios'],p4)
