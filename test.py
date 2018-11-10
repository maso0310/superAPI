import json
s = open('shopbuddy.json',encoding='utf-8')
line = s.readline()  #使用f.readline()得到的是字符串
result = json.loads(line)  #將字符串轉換爲字典
print(type(result))