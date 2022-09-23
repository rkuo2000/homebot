import requests

#url = 'http://127.0.0.1:5000/im_size'
#url = 'http://03fed875988c.ngrok.io/im_size' #if server running ngrok
url = 'http://127.0.0.1:5000/im_read'

my_img = {'image': open('test.jpg', 'rb')}
r = requests.post(url, files=my_img)

print(r.json())
