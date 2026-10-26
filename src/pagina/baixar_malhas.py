"""Baixa as malhas municipais (GeoJSON por UF, origem IBGE) do repositório tbrugz/geodata-br (CC0)
para dados/geo/origem/. Essa pasta não é versionada (26 MB); só a malha simplificada é."""
import pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / 'dados' / 'geo' / 'origem'; DEST.mkdir(parents=True, exist_ok=True)
UFS = [11,12,13,14,15,16,17,21,22,23,24,25,26,27,28,29,31,32,33,35,41,42,43,50,51,52,53]
URL = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-{c}-mun.json'
for c in UFS:
    out = DEST / f'g{c}.json'
    if out.exists(): continue
    urllib.request.urlretrieve(URL.format(c=c), out); print('baixado', out.name)
