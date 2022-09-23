### git clone https://github.com/line/line-bot-sdk-python
### cd line-bot-sdk-python
### cp ~/homebot/linebot_chatbot.py .
### (edit LINE_CHANNEL_ACCESS_TOKEN & LINE_CHANNEL_SECRET)
### cp ~/tf/intents.json .
### cp ~/tf/data.pickle .
### cp ~/tf/model/chatbot_dnn.h5 .
### python linebot_chatbot.py
from __future__ import unicode_literals

import os
import sys
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Flatten, Dense, Dropout
import random
import json
import pickle

#from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

app = Flask(__name__)
line_bot_api = LineBotApi('oty2ZNajxlkih7UI0L1vIA3pka0MX8wLphpRKampiW+DD7JWc4RH6leJvtzY90iLRsqksQYZVgH49ri6+mbXi/GeSr8xlIX/VR6MrXcMXdh+NqSU9o4F+EhNsooCfGyE+MiCyhUyslw+1p34hF1hkAdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('a3320043fa730f441f0e0442d681365a')

## for GPU
config=tf.ConfigProto(allow_soft_placement=True)
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
tf.keras.backend.set_session(sess)

with open("intents.json") as file:
    data = json.load(file)
with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

# Load Model
tf.keras.backend.clear_session()
model = keras.models.load_model('chatbot_dnn.h5')

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)
	
def chatbot(text):
    tf.keras.backend.clear_session()
    model = keras.models.load_model('chatbot_dnn.h5')
    results = model.predict(numpy.array([bag_of_words(text, words)]))
    print('confidence: '+str(numpy.max(results)*100))
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
			   
    return(random.choice(responses))
	
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        print(event.message.text)
		
        text = chatbot(event.message.text)
		
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text)
        )

    return 'OK'


if __name__ == "__main__":
#    arg_parser = ArgumentParser(
#        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
#    )
#    arg_parser.add_argument('-p', '--port', type=int, default=80, help='port')
#    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
#    options = arg_parser.parse_args()

#    app.run(debug=options.debug, port=options.port)
    app.run(host='0.0.0.0', port=80)
