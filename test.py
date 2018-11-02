import time
import re

text = "支出項目  吉普賽民歌餐廳240"
item = '項目.*'
money = '\d' 
pay_for = re.findall(item,text)
pay_money = re.findall(money,text)
pay_for_text = pay_for[0]
pay_money_text = pay_money[0]
date = time.strftime('%Y-%m-%d',time.localtime())

a = "已記錄"+date+"花費"+pay_for_text+pay_money_text+'元'
print(a)