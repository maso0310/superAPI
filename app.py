#店主店名
shop_name = 'MASO0310'
SessionauxData='R8957656'

#flask(不知道做啥的)
from flask import Flask, request, abort

#開啟各種API認證
#from config import *

#基礎模組
import time
import re
import csv
import requests
from bs4 import BeautifulSoup

#IMGUR上傳
from imgurpython import ImgurClient
import tempfile, os
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, \
    line_channel_secret

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

#Google表單
import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

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
    if "test" in msg:
        #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'LineBot.json'
        GSpreadSheet = 'LineBot'
        while True:
            try:
                scope = ["https://spreadsheets.google.com/feeds","https://accounts.google.com/o/oauth2/auth"]
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                worksheet = gc.open(GSpreadSheet).sheet1
                print("登入成功")
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt=""
            textt+=event.message.text
            if textt!="":
                worksheet.append_row((datetime.datetime.now(), textt))
                print('新增一列資料到試算表' ,GSpreadSheet)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
                return textt

    elif "支出" in msg: #輸入你預期使用者會輸入的部分
        #商品縮圖網址

        item = ' .*[\u4e00-\u9fa5]'
        money = '[0-9].*' 
        pay_for = re.findall(item,event.message.text)
        pay_money = re.findall(money,event.message.text)
        pay_for_text = pay_for[0][1:]
        pay_money_text = pay_money[0]
        print(pay_for_text)
        print(pay_money_text)
        date = time.strftime('%Y-%m-%d',time.localtime())
        '''
        with open('財務紀錄.csv',newline='', mode='a') as f:
            writer = csv.writer(f)
            writer.writerow([date,pay_for[0],pay_money[0]])
        '''
        a = "已記錄"+date+pay_for_text+pay_money_text+"元"
        b = date+pay_for_text+pay_money_text
        f = open('finance.txt','a')
        f.write(b+'\n')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
    
    elif "帳簿" in msg:
#        with open('財務紀錄.csv',mode='r',encoding='utf-8') as f:
#            for row in csv.DictReader(f):
#                a = row['日期']+row['項目']+row['金額']
        f = open('finance.txt','r',encoding='UTF-8')
        look = f.read()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=look))

    elif "全新生活問卷調查" in msg:
        output = image_carousel_message1('https://e.share.photo.xuite.net/fairc/1e0df66/5172143/260290231_m.jpg','健康飲食問卷調查','line://app/1610156977-prP8M5q8')
        line_bot_api.reply_message(event.reply_token,output)
#line://app/1610156977-prP8M5q8

    elif "Maso商城週年慶，感謝大家長期以來的支持" in msg:
        url = 'https://i.imgur.com/nMcOcAR.jpg?1'
        big_pic = image_carousel_message1(url,'填問卷送禮物','line://app/1610156977-x4KwQLJw')
        line_bot_api.reply_message(event.reply_token,big_pic)

    elif "來看看包裝精美的蒟蒻禮盒吧" in msg:
        img_url = 'https://i.imgur.com/UwmK8yX.png'
        p1_url = 'https://www.cheerspops.com.tw/%E8%92%9F%E8%92%BB%E5%87%8D.html'
        p2_url = 'line://app/1610156977-E6LyX0vy'
        p3_url = 'line://app/1610156977-KEOnxXen'
        p4_url = 'line://app/1610156977-XdeW1GqW'

        product = imagemap_message(img_url,p1_url,p1_url,p1_url,p1_url)
        print(type(product))
        line_bot_api.reply_message(event.reply_token,product)

    elif "Shop Buddy" in msg:
        shopbuddy = BubbleContainer(
            type="bubble",
            header=BoxComponent(
            type="box",
            flex= 0,
            spacing='md',
            layout="horizontal",
            contents= [
                TextComponent(
                type="text",
                text= "幫你節省荷包的超級好幫手",
                weight= "bold",
                color= "#009FCC",
                size= "lg"
                )
            ]
            ),
            hero=ImageComponent(
            type= "image",
            url= "https://i.imgur.com/cBCxtqM.jpg",
            size= "full",
            backgroundColor="#33FFFF",
            aspectRatio= "2:1",
            aspectMode= "fit",
            action= URIAction(
                type= "uri",
                uri= "https://tw.shop.com/"+shop_name+"/shopbuddy?credituser="+SessionauxData
            )
            ),
            body=BoxComponent(
            type= "box",
            layout= "horizontal",
            spacing= "sm",
            contents= [
                BoxComponent(
                type= "box",
                layout= "vertical",
                flex= 1,
                contents= [
                    ImageComponent(
                    type= "image",
                    url= "https://i.imgur.com/i51rNfd.jpg",
                    aspectMode= "cover",
                    aspectRatio= "4:3",
                    flex=0,
                    size= "md"
                    ),
                    ImageComponent(
                    type= "image",
                    url= "https://i.imgur.com/XEXfWvJ.jpg",
                    aspectMode= "cover",
                    aspectRatio= "4:3",
                    flex=1,
                    size= "md"
                    ),
                    ImageComponent(
                    type= "image",
                    url= "https://i.imgur.com/daZMJPn.jpg",
                    aspectMode= "cover",
                    aspectRatio= "4:3",
                    flex=2,
                    margin= "md",
                    size= "md"
                    )
                ]
                ),
                BoxComponent(
                type= "box",
                layout= "vertical",
                flex= 2,
                contents= [
                    TextComponent(
                    type= "text",
                    text= "操作步驟教學(使用電腦操作)",
                    gravity= "top",
                    size= "xxs",
                    flex= 1
                    ),
                    SeparatorComponent(
                    type= "separator"
                    ),
                    TextComponent(
                    type= "text",
                    text= "1.免費註冊為Shop.com顧客",
                    gravity= "center",
                    size= "xxs",
                    flex= 2
                    ),
                    SeparatorComponent(
                    type= "separator"
                    ),
                    TextComponent(
                    type= "text",
                    text= "2.用瀏覽器下載ShopBuddy",
                    gravity= "center",
                    size= "xxs",
                    flex= 2
                    ),
                    SeparatorComponent(
                    type= "separator"
                    ),
                    TextComponent(
                    type= "text",
                    text= "3.時時提醒您領取回饋金",
                    gravity= "bottom",
                    size= "xxs",
                    flex= 1
                    )
                ]
                )
            ]
            ),
            footer=BoxComponent(
            type= "box",
            layout= "horizontal",
            contents= [
                ButtonComponent(
                type= "button",
                action=URIAction(
                    type= "uri",
                    label= "立即註冊成為顧客累積回饋金",
                    uri= "https://tw.shop.com/"+shop_name+"/nbts/create-myaccount.xhtml?credituser="+SessionauxData+"&returnurl=https%3A%2F%2Ftw.shop.com%2F"
                )
                )
            ]
            )
        )
        message = FlexSendMessage(alt_text='最新購物工具！',contents=shopbuddy)
        print("https://tw.shop.com/"+shop_name+"/shopbuddy?credituser="+SessionauxData)
        line_bot_api.reply_message(event.reply_token,message)


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

#APP的main函數
@handler.add(MessageEvent, message=(ImageMessage))
def handle_message(event):
    #如果LINE用戶端傳送過來的是圖片
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
    if isinstance(event.message, ImageMessage):
    #先設定選擇的檔案附檔名
        ext = 'jpg'
        #擷取訊息內容
        message_content = line_bot_api.get_message_content(event.message.id)
        print(message_content)
        #建立臨時目錄
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        #將臨時目錄寫入路徑tempfile_path
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        #臨時路徑+副檔名
        dist_path = tempfile_path + '.' + ext
        #未知
        dist_name = os.path.basename(dist_path)
        #os.rename(old,new)將舊檔名改成新檔名
        os.rename(tempfile_path, dist_path)
        path = os.path.join('static', 'tmp', dist_name)
        print("接收到的圖片路徑："+path)

        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': 'UthLp77',
                'name': '2018/11/29',
                'title': 'uid',
                'description': 'Cute kitten being cute on '
            }
            client.upload_from_path(path, config=config, anon=False)
            #os.remove(path)
            #job =  q.fetch_job(result.id)
            #print(job.result)
        except:
            pass            
        return 0


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