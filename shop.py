import requests
from bs4 import BeautifulSoup
import re
keyword = 'HTC'

data={
    'st':keyword,
    'sy':'products'
}
url = 'https://tw.shop.com/search/header/'+keyword
res = requests.post(url,data=data)
print(res)
#cookies = {"CC_PORTALID":""}
