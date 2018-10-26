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
from Ten_Carousel import *

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
    if "偷偷回傳的訊息" in msg: #輸入你預期使用者會輸入的部分
        test = sticker_message(1,2)
        line_bot_api.reply_message(event.reply_token,test)

    elif "Cream Tea，開團！":
        #商品縮圖網址
        img_url = [
            'https://www.creamtea.com.tw/upload/product/201801251658180.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251712060.jpeg',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251652110.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251715090.JPG',
            'https://www.creamtea.com.tw/upload/product/201801251717160.JPG'
        ]

        #商品名稱
        title = [
            'CreamTea 9入家常檸檬塔',
            'CreamTea 8吋家常檸檬塔',
            'CreamTea 奶油茶原味組合-草莓果醬',
            'CreamTea 奶油茶原味組合-覆盆子果醬',
            'CreamTea 奶油茶原味組合-黑醋栗果醬',
            'CreamTea 奶油茶葡萄乾組合-草莓果醬',
            'CreamTea 奶油茶葡萄乾組合-覆盆子果醬',
            'CreamTea 奶油茶葡萄乾組合-黑醋栗果醬',
            'CreamTea 10入三溫糖蝴蝶酥',
            'CreamTea 20入三溫糖蝴蝶酥'
        ]

        #商品描述
        text1 = [
            '9入/盒',
            '8吋檸檬塔*1入 (約直徑20CM)',
            '原味司康*6入 / 自家手工凝結奶油*2入/ 英國TipTree草苺果醬*1',
            '原味司康*6入 / 自家手工凝結奶油*2入/ 英國TipTree覆盆子果醬*1',
            '原味司康*6入 / 自家手工凝結奶油*2入/ 英國TipTree黑醋栗果醬*1',
            '葡萄乾司康*6入 / 自家手工凝結奶油*2入/ 英國TipTree草莓果醬*1',
            '葡萄乾司康*6入 / 自家手工凝結奶油*2入/ 英國TipTree覆盆子果醬*1',
            '葡萄乾司康*6入 / 自家手工凝結奶油*2入/ 英國: Tip Tree 黑醋栗果醬*1',
            '10片裝/手提盒',
            '20片裝/盒'
        ]

        #單價
        label2 = [
            '$ 530',
            '$ 610',
            '$ 460',
            '$ 460',
            '$ 460',
            '$ 460',
            '$ 460',
            '$ 460',
            '$ 290',
            '$ 560'
        ]


        #我要購買的選項
        label3 = [
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1'
        ]

        #用戶回傳的訊息
        text3 = [
            'CreamTea 9入家常檸檬塔　+1',
            'CreamTea 8吋家常檸檬塔　+1',
            'CreamTea 奶油茶原味組合-草莓果醬　+1',
            'CreamTea 奶油茶原味組合-覆盆子果醬　+1',
            'CreamTea 奶油茶原味組合-黑醋栗果醬　+1',
            'CreamTea 奶油茶葡萄乾組合-草莓果醬　+1',
            'CreamTea 奶油茶葡萄乾組合-覆盆子果醬　+1',
            'CreamTea 奶油茶葡萄乾組合-黑醋栗果醬　+1',
            'CreamTea 10入三溫糖蝴蝶酥　+1',
            'CreamTea 20入三溫糖蝴蝶酥　+1'
        ]

        #更多詳細資訊
        label4 = [
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊',
            '更多詳細資訊'
        ]

        #使用者進入的網址
        url4 = [
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx',
            'https://www.creamtea.com.tw/tw/product/index.aspx'
        ]

        buy_together = Ten_Carousel_Template(
            img_url = [0],title = [0],text1 = [0],label2 = [0],label3 = [0],text3 = [0],label4 = [0],url4 = [0],
            img_url = [1],title = [1],text1 = [1],label2 = [1],label3 = [1],text3 = [1],label4 = [1],url4 = [1],
            img_url = [2],title = [2],text1 = [2],label2 = [2],label3 = [2],text3 = [2],label4 = [2],url4 = [2],
            img_url = [3],title = [3],text1 = [3],label2 = [3],label3 = [3],text3 = [3],label4 = [3],url4 = [3],
            img_url = [4],title = [4],text1 = [4],label2 = [4],label3 = [4],text3 = [4],label4 = [4],url4 = [4],
            img_url = [5],title = [5],text1 = [5],label2 = [5],label3 = [5],text3 = [5],label4 = [5],url4 = [5],
            img_url = [6],title = [6],text1 = [6],label2 = [6],label3 = [6],text3 = [6],label4 = [6],url4 = [6],
            img_url = [7],title = [7],text1 = [7],label2 = [7],label3 = [7],text3 = [7],label4 = [7],url4 = [7],
            img_url = [8],title = [8],text1 = [8],label2 = [8],label3 = [8],text3 = [8],label4 = [8],url4 = [8],
            img_url = [9],title = [9],text1 = [9],label2 = [9],label3 = [9],text3 = [9],label4 = [9],url4 = [9],
        )
        line_bot_api.reply_message(event.reply_token,buy_together)

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
    'https://pic.pimg.tw/k87110/1411026253-2090326290.jpg','你想做什麼','選擇以下功能',
    '搜尋附近地點','偷偷回傳的訊息',
    '紀錄位置','紀錄位置',
    '沒做什麼','https://pic.pimg.tw/k87110/1411026253-2090326290.jpg'
    )
    print(check_list)
    
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