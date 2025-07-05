import requests

url = "https://remoteok.com/api"
remoteok = requests.get(url)

if remoteok.status_code == 200:
    vagas = remoteok.json()[1:]
    #vagas_python = [v for v in vagas if 'python' in [tag.lower() for tag in v.get("tags", [])]]  #como filtrar

