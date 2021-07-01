import requests
url = 'http://192.168.1.7/post'

myobj = {'message': 'how are you'}

x = requests.post(url, data = myobj)

print(x.text)

