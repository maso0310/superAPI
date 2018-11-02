import time
import re

text = "支出項目  吉普賽民歌餐廳240"
item = '項目.*'
money = '\d' 
pay_for = re.findall(item,text)
pay_money = re.findall(money,text)
date = time.localtime()

a = "已記錄"+date
print(a)