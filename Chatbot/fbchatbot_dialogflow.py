#-*- coding: utf-8 -*-
#
# Homebot - api.ai
#
import os
import requests
from sys import argv
from bottle import Bottle, request
from bs4 import BeautifulSoup
import apiai
import json

FB_PAGE_TOKEN = "EAANFvjT1XoYBA"
FB_VERIFY_TOKEN = "verify me"
FB_GRAPH_API = 'https://graph.facebook.com/v2.12/me/messages?'
ApiAI_ACCESS_TOKEN = "9ef66045"

# Setup Bottle Server
app = Bottle()

@app.get('/')
def hello():
    return "Homebot: Hello !"

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
            if messages[0]:
                sender  = messages[0]['sender']['id']
                try:
                    message = messages[0]['message']
                    try:
                        text  = message['text']
                        print(text,sender)
                        api_ai(sender,text)
#-----------------------------------------------------------------------------
                    except KeyError:
                        print('>>>KeyError=message-text!')
                except KeyError:
                    print('>>>KeyError=message!')
    else:
        return 'Received Different Event'

def api_ai(sender,text):
    ai = apiai.ApiAI(ApiAI_ACCESS_TOKEN)
    request= ai.text_request()	
    request.query = text
    response = request.getresponse()
    reply = json.loads(response.read().decode())			
    msg=reply['result']['fulfillment']['speech']
    sendMessage(sender,msg)
	
def sendMessage(sender, text):
	"""
	Function for sending message
	"""
	data = {
		'recipient':{'id': sender},
		'message'  :{'text': text}
	}
	qs = 'access_token=' + FB_PAGE_TOKEN
	resp = requests.post(FB_GRAPH_API + qs, json=data)
	return resp.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=argv[1])
