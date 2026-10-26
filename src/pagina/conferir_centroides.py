import json,sys,pandas as pd
d=pd.read_csv(__import__('pathlib').Path(__file__).resolve().parents[2]/'dados'/'zonas_2026_t1_t2.csv'); d=d[d.cod_ibge.notna()]
ids=d.groupby(d.cod_ibge.astype(int)//100000).cod_ibge.apply(lambda s:set(s.astype(int)))
for f in sys.argv[1:]:
    j=json.load(open(f))
    for k,s in j.items():
        prev=0;got=set();bad=0
        for tok in s.split(' '):
            a=tok.split(','); prev+=int(a[0]); got.add(prev)
            x,y=int(a[1]),int(a[2])
            if not(-3700<x<-1700 and -1500<y<260): bad+=1
        want=ids[int(k)]
        print(k,len(got),len(want),'missing_in_cen',sorted(want-got)[:5],'extra',sorted(got-want)[:5],'badcoord',bad)
