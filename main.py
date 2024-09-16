import requests

base_url = "https://www.bitmex.com/api/v1"

r = requests.get(base_url)

returns = r.json()

print(returns)
