# update.py
import re

from urllib.request import urlopen

from bs4 import BeautifulSoup

def get_cheapest(url, text):
    with urlopen(url) as response:
        soup = BeautifulSoup(response.read(),'html.parser')

    cheapest_price = cheapest_item = None

    re_price = re.compile(r'\$(\d+)')
    root = soup.find('td', text=re.compile(text)).parent

    for option in root.find_all('option', text=re_price):
        item = option.text.strip()
        price = int(re_price.search(item).group(1))
        if cheapest_price is None or price < cheapest_price:
            cheapest_price = price
            cheapest_item = item

    return (cheapest_item, cheapest_price)

coolpc_url = 'http://www.coolpc.com.tw/evaluate.php'
ram_text = '記憶體 RAM'

(cheapest_item, cheapest_price) = get_cheapest(coolpc_url, ram_text)