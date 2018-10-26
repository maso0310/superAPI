import requests
from bs4 import BeautifulSoup

keyword = '海苔先生'
search_partner_store = 'site:mtwebcenters.com.tw'
url = 'https://www.google.com.tw/search?q='+keyword+search_partner_store
res = requests.get(url)
print(url)

parser = BeautifulSoup(res.text,'html.parser')
a=[]
soup = parser.find('cite')
print(soup.text)

target_partner_store = soup.text
partner_store_url = 'https://'+target_partner_store+'ecommerce/'

res_p =  requests.get(partner_store_url)
body = BeautifulSoup(res_p.text,'html.parser')

img_url = []#商品縮圖網址
title = []#商品名稱+單價
text1 = []#商品描述
label3 = []#我要購買的選項
text3 = []#用戶回傳的訊息
label4 = []#更多詳細資訊
url4 = []#更多詳細資料頁面


img_url_find = body.find_all('a','product-image')

for s in img_url_find:
    img_url.append(s)
print(img_url)
