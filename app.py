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
            '活動到11/08，3條免運，9條288/條，18條278/條，36條266/條',
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
            img_urlK[0],titleK[0],text1K[0],label4K[0],url4K[0],
            img_urlK[1],titleK[1],text1K[1],label4K[1],url4K[1],
            img_urlK[2],titleK[2],text1K[2],label4K[2],url4K[2],
            img_urlK[3],titleK[3],text1K[3],label4K[3],url4K[3],
            img_urlK[4],titleK[4],text1K[4],label4K[4],url4K[4],
            img_urlK[5],titleK[5],text1K[5],label4K[5],url4K[5]
            )
        partner_store = (msg1)
        line_bot_api.reply_message(event.reply_token,partner_store)



    elif "這樣更簡單明瞭一點" in msg:
        url = 'https://i.imgur.com/8O8fwXP.jpg'
        big_pic = image_carousel_message(url,'填寫訂購表單','line://app/1610156977-3Wv1zqb1')
        line_bot_api.reply_message(event.reply_token,big_pic)


    elif "HTC UU" in msg:
        cookies = {
            'LAST_CCSYN_SRC':'FAMOS',
            'LAST_CCSYN':'13663',
            'CC_DISTID':'891059297',
            '_abck':'D4AAB695B1988CB5DFF906FAE8D7AC8517D2D7267F070000149BC85BC781872B~-1~fTMkdH1HnwlA0PZsQHApzW1kLXGOOMgYOIglnksTAnE=~-1~-1',
            'AMID':'3470255176',
            'CATALOGCITY_SSNLIVE13663':'3470255176',
            'CC_SRCID':'2791',
            'SHOPLOCAL_PROMO_SEEN':'0',
            'SHOPMF_NS_ID':'185',
            'PROMO_ACQUISITION_ELIGIBLE':'false',
            'bm_sz':'D6B8A07350EE80CB065EB5FF78E202DC~QAAQz1evi8AnnNJmAQAA7NDe5BVIRsAJUZC3BPAt8acPj+aBpSh5cBtX0sPo0cLHHs6fjOsIHY0dX4HWinPtVGMdIpzQOb0dN75sKSsSszzilfWHDE7Cx8rZ5/0PNHEVVCQw4QTLAD231QdTVLjs+jupT+lKysQNjlIIAhS7Y8+a5Oe49154oNULnPRb',
            'ak_bmsc':'D4E7FAF5274A0E4FFA1072BF884E41A48BAF57CFC44A0000947AE05B0C057C1D~plnpIHXksDVvxmjs8ylwPtcWmLK75xmHi/EJQEuvv+tEi/BygrJDgAjXVQPcU9LdeXp0pxo6bhoBR7f7IlECICoEpXtAVEvCObKZNJH/tQ99MhObdhbWLEvs4Jd4BZkmt+vs70oOPqaQMhcFrHYaiPkThXDdX/hTN1BZl+a/umUBMmq+fnp/apJM9DX7F4wUfS93Zgo+dlmq2iLmm4UF6lXOooIzA3fxGgybD3b3HRd70=',
            'bm_mi':'4B54D2638122BB5BEDB097DB10FAD414~IcPPCDqSlsIelbmyfvh1DZYieg8pkiTMaoJFeSRfRQzLXgwfT8j9DO49PomVUMhrYAg5jxZu9FXMlo+t0+3YTrSiabBsm00hg0uMMvQ+g0LmdUgBkJjq6X/kWQzUguZ/J/BGwhR3kqf026QaLtRgiKbHx2ywvTfXZ3e63HhtBYv23cPQ3RLsMLNTdCp4ou2LRXB0NAt8colcIOYYqp8E8kSSoWdsjafjy5/SU/QW3hw=',
            'bm_sv':'0C0DB48FE47F6D1908FDCADCA90D10B3~3oyRYXQguDSiFrZWoRi8QVsoVSkISQWYdOY26Cy/UuoeDjwOCKkfYTd8WnhIBL+x6tOyldlYuNvNpvXNBz3xn/AuM9m/7o+tDmUnW0lVLr3/ztrNkSkH3t+wt3ps1W4TXU4u1+BhKH0OMiBs6DUpHg==',
            'JSESSIONID':'8562CEE10AA61DA99234DE54B92D2408',
            'CC_PORTALID':'1345008',
            'AMOS_OKTOCACHE':'false',
            'COUNTRY_MATCH':'true'
        }

        headers = {
            'Server':'Apache-Coyote/1.1',
            'Content-Type':'text/html;charset=UTF-8',
            'Content-Language':'zh-TW',
            'Content-Encoding':'gzip',
            'Vary':'Accept-Encoding',
            'Strict-Transport-Security':'max-age=63072000',
            'X-Akamai-Transformed':'9 24850 0 pmb=mTOE,3',
            'Connection':'keep-alive',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://tw.shop.com/',
            'upgrade-insecure-requests': '1'
        }

        data={
            'st':event.message.text,
            'sy':'products'
        }
        url = 'https://tw.shop.com/search/header/'+event.message.text
        res = requests.post(url,data=data,headers=headers,cookies=cookies)
        print(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res.text))

    elif "我是誰" in msg:
        message = FlexSendMessage(
            altText="test",
            contents=BubbleContainer(
            header=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=uid,
                        weight='bold',
                        color='#aaaaaa',
                        size='lg'
                    )
                ]
            ),
            hero=ImageComponent(
                size='lg',
                url=profile.picture_url
            )
        ))
        line_bot_api.reply_message(event.reply_token,message)

     
    elif "來看看包裝精美的蒟蒻禮盒吧" in msg:
        img_url = 'https://i.imgur.com/UwmK8yX.png'
        p1_url = 'https://www.cheerspops.com.tw/%E8%92%9F%E8%92%BB%E5%87%8D.html'
        p2_url = 'line://app/1610156977-E6LyX0vy'
        p3_url = 'line://app/1610156977-KEOnxXen'
        p4_url = 'line://app/1610156977-XdeW1GqW'

        product = imagemap_message(img_url,p1_url,p1_url,p1_url,p1_url)
        print(type(product))
        line_bot_api.reply_message(event.reply_token,product)

    elif "最新公告" in msg:
        s = {
            "type": "bubble",
            "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                "type": "text",
                "text": "幫你大大節省荷包好幫手",
                "weight": "bold",
                "color": "#aaaaaa",
                "size": "sm"
                }
            ]
            },
            "hero": {
            "type": "image",
            "url": "https://i.imgur.com/7cCG7dd.jpg?1",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "fit",
            "action": {
                "type": "uri",
                "uri": "line://app/1610156977-pYOvGD5v"
            }
            },
            "body": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "md",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "flex": 1,
                "contents": [
                    {
                    "type": "image",
                    "url": "https://i.imgur.com/i51rNfd.jpg",
                    "aspectMode": "cover",
                    "aspectRatio": "4:3",
                    "size": "sm",
                    "gravity": "bottom"
                    },
                    {
                    "type": "image",
                    "url": "https://i.imgur.com/daZMJPn.jpg",
                    "aspectMode": "cover",
                    "aspectRatio": "4:3",
                    "margin": "md",
                    "size": "sm"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "vertical",
                "flex": 2,
                "contents": [
                    {
                    "type": "text",
                    "text": "操作步驟教學(電腦介面)",
                    "gravity": "top",
                    "size": "xs",
                    "flex": 1
                    },
                    {
                    "type": "separator"
                    },
                    {
                    "type": "text",
                    "text": "1.註冊為Shop.com免費顧客",
                    "gravity": "center",
                    "size": "xs",
                    "flex": 2
                    },
                    {
                    "type": "separator"
                    },
                    {
                    "type": "text",
                    "text": "2.用瀏覽器下載ShopBuddy",
                    "gravity": "center",
                    "size": "xs",
                    "flex": 2
                    },
                    {
                    "type": "separator"
                    },
                    {
                    "type": "text",
                    "text": "3.若有回饋金將會即刻提醒",
                    "gravity": "bottom",
                    "size": "xs",
                    "flex": 1
                    }
                ]
                }
            ]
            },
            "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "立即註冊成為顧客累積回饋金",
                    "uri": "line://app/1610156977-YDl9J6O9"
                }
                }
            ]
            }
        }
        j = FlexSendMessage(altText='最新購物工具！')
        line_bot_api.reply_message(event.reply_token,j)


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