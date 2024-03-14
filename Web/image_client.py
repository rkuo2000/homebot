import requests

url = 'http://127.0.0.1:8000/image'

my_img = {'image': open('test.jpg', 'rb')}
r = requests.post(url, files=my_img)

print(r.json())
