### git clone https://github.com/line/line-bot-sdk-python
### cd line-bot-sdk-python
### cp ~/homebot/linebot_echo.python
### python linebot_echo.py
from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('oty2ZNajxlkih7UI0L1vIA3pka0MX8wLphpRKampiW+DD7JWc4RH6leJvtzY90iLRsqksQYZVgH49ri6+mbXi/GeSr8xlIX/VR6MrXcMXdh+NqSU9o4F+EhNsooCfGyE+MiCyhUyslw+1p34hF1hkAdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('a3320043fa730f441f0e0442d681365a')

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

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=80, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
