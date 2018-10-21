#flask(不知道做啥的)
from flask import Flask, request, abort

#開啟各種API認證
#from config import *

#JSON編碼解碼
import json

#lineAPI
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#AI自然語言分析(DialogFlow)
import apiai

app = Flask(__name__)

#LINEAPI認證
line_bot_api = LineBotApi('TNwu7tqho7m8MnMSmG8jpAF8tWl+hzBQzb/JKdbDBJv3HkMAUJiz8uo0nS0hG89tbsjQk8IV02p/v5ChZ1txRKjMlvPufgBPak5Y5AEwJt84wc9Mocg+yeZ8oyRQcfwFKnfmNaNRJR27Qc9r6iY38AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d184dfc3ec38e22fb7edf6b7275023a8')



# 監聽所有來自 /callback 的 Post Request
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

# ================= API語言客製區 Start =================
def is_alphabet(uchar):
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        print('English')
        return "en"
    elif '\u4e00' <= uchar<='\u9fff':
        #print('Chinese')
        print('Chinese')
        return "zh-tw"
    else:
        return "en"
# ================= API語言客製區 End =================


# ================= 獲得使用者訊息 =================
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    profile = line_bot_api.get_profile
    print(event.message.text)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    print(profile.display_name)
    msg = event.message.text # message from user

    # 1. 傳送使用者輸入到 dialogflow 上
    ai_request = ai.text_request()
    #ai_request.lang = "en"
    ai_request.lang = is_alphabet(msg)
    ai_request.query = msg



    # 2. 獲得使用者的意圖
    ai_response = json.loads(ai_request.getresponse().read())
    user_intent = ai_response['result']['metadata']['intentName']

    # 3. 根據使用者的意圖做相對應的回答
    if msg == "": # 當使用者意圖為詢問午餐時
        # 建立一個 button 的 template
        buttons_template_message = TemplateSendMessage(
            alt_text="Please tell me where you are",
            template=ButtonsTemplate(
                text="Please tell me where you are",
                actions=[
                    URITemplateAction(
                        label="Send my location",
                        uri="line://nv/location"
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message)

    #以下code用來蒐集使用者錯誤的訊息來加強訓練
    elif msg == "讀取錯誤": # 讀取error_text的內容
        f = open('error_text.txt','r', encoding='UTF-8')
        look = f.read()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=look))

    elif msg == "刪除錯誤": # 刪除error_text的內容
        f = open('error_text.txt','w')

    else: # 聽不懂時在error_text做紀錄
        f = open('error_text.txt','a')
        f.write(msg+'\n')
'''
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
'''
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
