import requests

path = "http://192.168.0.20"

r = requests.get(path)
print(r.text)
