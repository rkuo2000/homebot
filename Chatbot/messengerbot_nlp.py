# chatbot for FB Messenger with NLP
import os
import requests
from sys import argv
from bottle import Bottle, request
from bs4 import BeautifulSoup
import json
import re

FB_ACCESS_TOKEN = "EAAeaXj2tnk0BAFJ7ObKVy..................."
FB_VERIFY_TOKEN = "verify me"
FB_GRAPH_API = 'https://graph.facebook.com/v3.2/me/messages?'

# Setup Bottle Server
app = Bottle()

@app.get('/')
def hello():
    return "Homedroid: Hello !"

@app.get('/webhook')
def messenger_webhook():
	verify_token = request.query.get('hub.verify_token')
	if verify_token == FB_VERIFY_TOKEN:
		return request.query.get('hub.challenge')
	else:
		return 'Invalid Request or Verification Token'

@app.post('/webhook')
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            messages = entry['messaging']
            #print(messages)
            if messages[0]:
                sender  = messages[0]['sender']['id']
                try:
                    message = messages[0]['message']
#-------------------Message Text-----------------------------------------------
                    try:
                        text  = message['text']
                        #sendMessage(sender, text) # echo back
                        print(sender, text)
                        nlp   = message['nlp']
                        #print(nlp)
                        #print(nlp['entities']['sentiment'][0]['value'])
                        try:
                            greetings=nlp['entities']['greetings']
                            greeting=nlp['entities']['greetings'][0]
                            print(greeting['confidence'],greeting['value'])
                            sendMessage(sender, 'I am homedroid, how may I help you?') # reply
                        except KeyError:
                            sendMessage(sender, text) # echo back
                            #print('>>>KeyError=No_Greetings!')
                    except KeyError:
                        print('>>>KeyError=message-text!')
                    except KeyError:
                        print('>>>KeyError=message-quick_reply!')
                except KeyError:
                    print('>>>KeyError=message!')
                except KeyError:
                    print('>>>KeyError=postback!')
    else:
        return 'Received Different Event'

def sendMessage(sender, text):
	"""
	Function for sending message
	"""
	data = {
		'recipient':{'id': sender},
		'message'  :{'text': text}
	}
	qs = 'access_token=' + FB_ACCESS_TOKEN
	resp = requests.post(FB_GRAPH_API + qs, json=data)
	return resp.content
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=argv[1])
