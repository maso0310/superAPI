#flask(不知道做啥的)
from flask import Flask, request, abort

#開啟各種API認證
#from config import *

#基礎模組
import time

#JSON編碼解碼
import json

#lineAPI
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from MessageForm import *

#AI自然語言分析(DialogFlow)
import apiai

app = Flask(__name__)

#LINEAPI認證
ai = apiai.ApiAI('084bce6e157c47d39d5cb23715b47b69')
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
    print(event.message.text)
    msg = event.message.text # message from user
    uid = event.source.user_id # user id
    
    # 1. 傳送使用者輸入到 dialogflow 上
    ai_request = ai.text_request()
    #ai_request.lang = "en"
    ai_request.lang = is_alphabet(msg)
    ai_request.session_id = uid
    ai_request.query = msg
    try:
        profile = line_bot_api.get_profile(uid)
        print(profile.display_name)
        print(profile.status_message)
        print(uid)
        print(profile.picture_url)
    except LineBotApiError as e:
        #error handle 
        print(e)

    # 2. 獲得使用者的意圖
    ai_response = json.loads(ai_request.getresponse().read())
    user_intent = ai_response['result']['metadata']['intentName']
    print(user_intent)

    # 3. 根據使用者的意圖做相對應的回答
    if "test" in msg: #輸入你預期使用者會輸入的部分
        test = sticker_message(1,2)
        line_bot_api.reply_message(event.reply_token,test)

    elif "餐廳，" in msg:
        ask_place = TemplateSendMessage(
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
        line_bot_api.reply_message(event.reply_token,buttons_template_message)

        from nearbyplace import restaurant
        good_restaurant = restaurant()





#========================以下code用來蒐集使用者錯誤的訊息來加強訓練

    elif msg == "讀取錯誤": # 讀取error_text的內容
        f = open('error_text.txt','r', encoding='UTF-8')
        look = f.read()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=look))

    elif msg == "刪除錯誤": # 刪除error_text的內容
        f = open('error_text.txt','w')

    else: # 聽不懂時在error_text做紀錄
        f = open('error_text.txt','a')
        f.write(event.message.text+'\n')
#===============================================================

#處理位置訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    check_list = buttons_message(
    'https://cdn.shopify.com/s/files/1/1285/0147/products/sign2-032a_b926f437-6ca3-4b1f-abd4-172576b75ca6.png?v=1527227219','你想做什麼','選擇以下功能',
    '搜尋附近地點','搜尋地點','這要寫什麼?',
    '紀錄位置','紀錄位置',
    '沒做什麼','url1'
    )
    line_bot_api.reply_message(event.reply_token,check_list)

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

    #以下為有待開發的功能列
    #elif "筆記，" in msg:
    #elif "行事曆，" in msg:
    #elif "計程車，" in msg:
    #elif "youtube，" in msg:
    #elif "火車，" in msg:
    #elif "航班，" in msg:
    #elif "facebook，" in msg:
    #elif "八卦版，" in msg:
    #elif "健康，" in msg:
    #elif "健身，" in msg:
    #elif "活動，" in msg:
    #elif "政策，" in msg:
    #elif "加油站，" in msg:
    #elif "郵遞區號，" in msg:
    #elif "職缺，" in msg:
    #elif "廣播，" in msg:
    #elif "每日優惠，" in msg:
    #elif "揪團購，" in msg:
    #elif "辦活動，" in msg:
    #elif "食譜，" in msg:
    #elif "遊戲，" in msg:
    #elif "運動新聞，" in msg:
    #elif "比價，" in msg:
    #elif "瑜珈，" in msg:
    #elif "放鬆，" in msg:
    #elif "輕音樂，" in msg:
    #elif "猜謎，" in msg:
    #elif "骰子，" in msg: