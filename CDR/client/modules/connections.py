import requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'

path = "localhost"

payload = {
    "uid" : "uid",
}
r = requests.get(path, params=payload)
print(r.url)
