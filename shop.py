import requests
from bs4 import BeautifulSoup
import re
keyword = 'HTC'
url = 'https://tw.shop.com/maso0310/'+keyword



res_get = requests.get(url)
print(res_get)
soup_get = BeautifulSoup(res_get.text,'html.parser')
image = soup_get.find('img')
for src in image:
    print(src)
