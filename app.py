# encoding: utf-8
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationMessage,
)


app = Flask(__name__)

# 使用環境變數，避免資料外洩
handler = WebhookHandler(os.environ['CHANNEL_SECRET']) 
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN']) 

@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# ================= 機器人區塊 Start =================
@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
    msg = event.message.text #message from user

    # 針對使用者各種訊息的回覆 Start =========
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

    # 針對使用者各種訊息的回覆 End =========

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 獲取使用者的經緯度
    lat = event.message.latitude
    long = event.message.longitude
    msg = "lat: {}; long: {}".format(lat, long)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
 
# ================= 機器人區塊 End =================

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ['PORT']))