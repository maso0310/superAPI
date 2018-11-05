#flask(不知道做啥的)
from flask import Flask, request, abort

#開啟各種API認證
#from config import *

#基礎模組
import time
import re
import csv

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
    if "表單" in msg:
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
    
    elif "亞尼克揪團" in msg:
        img_url = [
            'https://i.imgur.com/8O8fwXP.jpg',
            'https://i.imgur.com/HJvuelW.jpg',
            'https://i.imgur.com/9SDPC5u.jpg',
            'https://i.imgur.com/XJibX7m.jpg',
            'https://i.imgur.com/QRuEwE3.jpg',
            'https://i.imgur.com/P2MmiCv.jpg',
            'https://i.imgur.com/cXAvKwC.jpg'
        ]

        #商品名稱
        title = [
            '美安大會亞尼克生乳捲優惠資訊',
            '亞尼克生乳捲-極致黑  原價450$/條',
            '亞尼克生乳捲-靜岡抹茶  原價420$/條',
            '亞尼克生乳捲-特黑巧克力  原價380/條',
            '亞尼克生乳捲-原味  原價380/條',
            '亞尼克生乳捲-黑魔粒雙漩  原價420$/條',
            '亞尼克起司磚-原味  原價380$/條'
        ]

        #商品描述
        text1 = [
            '活動期間11/01~11/11，3件以上免運，越多越便宜',
            '《獨家商品》天然竹炭粉捲入北海道奶霜與糖炒芝麻交融的美味。',
            '奢侈地使用日本靜岡製造的高級抹茶粉，香氣深厚濃郁。',
            '來自北海道的乳源，成就豐厚芳醇的自然風味。 ',
            '來自北海道的乳源，成就豐厚芳醇的自然風味。',
            '結合脆粒分明的巧克力豆，北海道奶霜裡蘊藏著醇厚的巧克力香氣！',
            '剛入口的起司帶點口感與焦香，是義大利帕達諾起司醇厚的風味。'
        ]


        #更多詳細資訊
        label4 = [
            '立即填寫團購表單',
            '商品詳細資訊',
            '商品詳細資訊',
            '商品詳細資訊',
            '商品詳細資訊',
            '商品詳細資訊'
        ]

        #使用者進入的網址
        url4 = [
            'line://app/1610156977-3Wv1zqb1',
            'http://buy.yannick.com.tw/product.php?pid_for_show=4100',
            'http://buy.yannick.com.tw/product.php?pid_for_show=4099',
            'http://buy.yannick.com.tw/product.php?pid_for_show=4098',
            'http://buy.yannick.com.tw/product.php?pid_for_show=4097',
            'http://buy.yannick.com.tw/product.php?pid_for_show=4096'
        ]

        msg1 = Ten_Carousel_Template(
            img_url[0],title[0],text1[0],label4[0],url4[0],
            img_url[1],title[1],text1[1],label4[1],url4[1],
            img_url[2],title[2],text1[2],label4[2],url4[2],
            img_url[3],title[3],text1[3],label4[3],url4[3],
            img_url[4],title[4],text1[4],label4[4],url4[4],
            img_url[5],title[5],text1[5],label4[5],url4[5]
        )

        img_urlK = [
            'https://www.give-me-the-money.com/_imagecache/%E6%9C%AA%E5%91%BD%E5%90%8D.jpg',
            'https://i.imgur.com/bpYXSFr.jpg',
            'https://i.imgur.com/SxDWzYq.jpg',
            'https://i.imgur.com/YrOY6PY.jpg',
            'https://i.imgur.com/w6IsmPx.jpg',
            'https://i.imgur.com/89U2tMG.jpg'
        ]

        #商品名稱
        titleK = [
            '宮崎水產新鮮肉品火鍋優惠資訊',
            '骰子牛大包裝3包入  890$免運',
            '懷舊牛肉爐3包入  1299$免運',
            '頂級智利鮭魚+厚片土魠魚各3片  1489$免運',
            '宮崎肉多多羊肉爐3包組  1468$免運',
            '滿2000加購人蔘烏骨雞湯買一送一  450$'
        ]

        #商品描述
        text1K = [
            '多種品項優質肉品一試成主顧',
            '骰子牛360g(包)',
            '懷舊牛肉爐1250g(包)',
            '鮭魚375g(片)土魠魚300g(片)',
            '肉多多羊肉爐1250g(包)',
            '人蔘雞湯2800g(包)'
        ]

        #我要購買的選項
        label3K = [
            '看全系列商品',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1',
            '我要+1'
        ]

        #用戶回傳的訊息
        text3K = [
            '宮崎水產官網 https://reurl.cc/Kxq6R',
            '大包裝骰子牛3入+1',
            '懷舊牛肉爐3入+1',
            '鮭魚土魠魚3入組合+1',
            '肉多多羊肉爐+1',
            '滿2000加購人蔘雞湯+1'
        ]

        #更多詳細資訊
        label4K = [
            '瞭解詳情',
            '瞭解詳情',
            '瞭解詳情',
            '瞭解詳情',
            '瞭解詳情',
            '瞭解詳情'

        ]

        #使用者進入的網址
        url4K = [
            'https://www.give-me-the-money.com/',
            'https://www.give-me-the-money.com/ecommerce/3/20.html',
            'https://www.give-me-the-money.com/ecommerce/13/117.html',
            'https://www.give-me-the-money.com/ecommerce/25-324/169.html',
            'https://www.give-me-the-money.com/ecommerce/13/73.html',
            'https://www.give-me-the-money.com/ecommerce/24-324/183.html'
        ]

        msg2 = Ten_Carousel_Template(
            img_urlK[0],titleK[0],text1K[0],label3K[0],text3K[0],label4K[0],url4K[0],
            img_urlK[1],titleK[1],text1K[1],label3K[1],text3K[1],label4K[1],url4K[1],
            img_urlK[2],titleK[2],text1K[2],label3K[2],text3K[2],label4K[2],url4K[2],
            img_urlK[3],titleK[3],text1K[3],label3K[3],text3K[3],label4K[3],url4K[3],
            img_urlK[4],titleK[4],text1K[4],label3K[4],text3K[4],label4K[4],url4K[4],
            img_urlK[5],titleK[5],text1K[5],label3K[5],text3K[5],label4K[5],url4K[5]
            )
        partner_store = (msg1)
        line_bot_api.reply_message(event.reply_token,partner_store)



    elif "威淨SNAP酵素清潔劑，開團！" in msg:
        #商品縮圖網址
        img_url = [
            'https://img.shop.com/Image/240000/246300/246302/products/809481173__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/1531559443__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/644795691__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/644795692__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/644795688__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/959119034__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/1294104564__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/644795689__2400x2400__.jpg',
            'https://img.shop.com/Image/240000/246300/246302/products/1660900392__2400x2400__.jpg',
            'https://img.shop.com/Image/250000/250600/250614/products/1660900448__2400x2400__.jpg'

        ]

        #商品名稱
        title = [
            '威淨™ 家潔組  NT$1,935',
            '威淨™居家清潔易潔包組（含專用瓶）  NT$1,590',
            '威淨™強力酵素高效洗衣精  NT$455',
            '威淨™強效清潔劑  NT$410',
            '威淨™萬用天然濃縮清潔劑  NT$420',
            '威淨™深層去污清潔劑  NT$420',
            '威淨™去味除漬噴霧  NT$410',
            '威淨™蘆薈洗碗精  NT$410',
            '威淨™洗衣易潔包–清新配方  NT$515',
            '愛的奇蹟™ 洗衣易潔包－無香精配方  NT$515'
        ]

        #商品描述
        text1 = [
            '全家清潔一次打包'+'\n'+'威淨®家潔組',
            '方便快速的新型溶劑'+'\n'+'含威淨™濃縮清潔易潔包組(與專用噴頭) ',
            '用酵素分解髒汙'+'\n'+'單瓶裝（1.183公升）',
            '油汙水漬輕鬆搞定'+'\n'+'單瓶裝（946毫升）',
            '溫和有效的萬用洗劑'+'\n'+'單瓶裝（946毫升)',
            '浴廁清潔深層去汙'+'\n'+'單瓶裝（946毫升)',
            '異味污漬輕鬆去除'+'\n'+'單瓶裝（236.5毫升）',
            '泡沫超多不傷雙手'+'\n'+'單瓶裝（946毫升）',
            '方便使用輕鬆洗淨'+'\n'+'單罐 (24包裝)',
            '適合清洗嬰幼兒衣物'+'\n'+'單罐 (24包裝)'
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
            '威淨™ 家潔組　+1',
            '威淨™居家清潔易潔包組　+1',
            '威淨™強力酵素高效洗衣精　+1',
            '威淨™強效清潔劑　+1',
            '威淨™萬用天然濃縮清潔劑　+1',
            '威淨™深層去污清潔劑　+1',
            '威淨™去味除漬噴霧　+1',
            '威淨™蘆薈洗碗精　+1',
            '威淨™洗衣易潔包–清新配方　+1',
            '愛的奇蹟™ 洗衣易潔包－無香精配方　+1'
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
            'http://t.cn/EZCiEdn',
            'http://t.cn/EZCiBuc',
            'http://t.cn/EZC6ZvA',
            'http://t.cn/EZC6ygI',
            'http://t.cn/EZC6qEK',
            'http://t.cn/EZC6fmN',
            'http://t.cn/EZC6i7h',
            'http://t.cn/EZC6Smo',
            'http://t.cn/EZC6NNS',
            'http://t.cn/EZC6lr8'
        ]

        buy_together = Ten_Carousel_Template(
            img_url[0],title[0],text1[0],label3[0],text3[0],label4[0],url4[0],
            img_url[1],title[1],text1[1],label3[1],text3[1],label4[1],url4[1],
            img_url[2],title[2],text1[2],label3[2],text3[2],label4[2],url4[2],
            img_url[3],title[3],text1[3],label3[3],text3[3],label4[3],url4[3],
            img_url[4],title[4],text1[4],label3[4],text3[4],label4[4],url4[4],
            img_url[5],title[5],text1[5],label3[5],text3[5],label4[5],url4[5],
            img_url[6],title[6],text1[6],label3[6],text3[6],label4[6],url4[6],
            img_url[7],title[7],text1[7],label3[7],text3[7],label4[7],url4[7],
            img_url[8],title[8],text1[8],label3[8],text3[8],label4[8],url4[8],
            img_url[9],title[9],text1[9],label3[9],text3[9],label4[9],url4[9]
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