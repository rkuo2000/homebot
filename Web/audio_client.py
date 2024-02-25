## To run server: python audio_server.py
## To run client: python audio_client.py

import requests

url = "http://127.0.0.1:8000/audio"

my_audio = {'audio': open("audio.mp4", "rb")}

r = requests.post(url, files=my_audio)

print(r.json())
