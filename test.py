import csv

with open('財務紀錄.csv',mode='r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)