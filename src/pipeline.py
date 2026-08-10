import requests
import json

url = "https://apisidra.ibge.gov.br/values/t/4709/n6/2611606/p/2022/v/93"

resposta = requests.get(url, timeout=10)

dados = resposta.json()

print(json.dumps(dados, indent=4, ensure_ascii=False))
