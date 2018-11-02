import csv

with open('財務紀錄.csv',mode='r',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        print(row)