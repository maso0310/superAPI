import csv
put = []
with open('財務紀錄.csv',mode='r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        a=row[0]
        b=row[1]
        c=row[2]
        print(a,b,c)
        d = a+b+c
        put.append(d)
    print(d[1])
print(put)
