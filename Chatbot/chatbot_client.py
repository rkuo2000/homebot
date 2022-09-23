### Run chabot server to receive text and reply
# usage: winpty python chatbot_sever.py

### Run chatbot client to send text
# usage: winpty python chatbot_client.py
import requests

url = 'http://127.0.0.1:5000/chat?text='

text = 'how are you doing'
resp = requests.post(url+text)
print(resp.text)
