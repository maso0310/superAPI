import csv

with open('財務紀錄.csv',mode='r',encoding='utf-8') as f:
    d = []
    for row in csv.DictReader(f):
        a = row['日期']+row['項目']+row['金額']
        print(a)