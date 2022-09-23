import requests
url = 'http://192.168.1.7/get?message='+'How Are You'

x = requests.get(url)

print(x.text)

