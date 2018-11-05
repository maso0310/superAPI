import requests
from bs4 import BeautifulSoup
import re
keyword = 'HTC'

cookies = {
    'LAST_CCSYN_SRC':'FAMOS',
    'LAST_CCSYN':'13663',
    'CC_DISTID':'891059297',
    '_abck':'D4AAB695B1988CB5DFF906FAE8D7AC8517D2D7267F070000149BC85BC781872B~-1~fTMkdH1HnwlA0PZsQHApzW1kLXGOOMgYOIglnksTAnE=~-1~-1',
    'AMID':'3470255176',
    'CATALOGCITY_SSNLIVE13663':'3470255176',
    'CC_SRCID':'2791',
    'SHOPLOCAL_PROMO_SEEN':'0',
    'SHOPMF_NS_ID':'185',
    'PROMO_ACQUISITION_ELIGIBLE':'false',
    'bm_sz':'D6B8A07350EE80CB065EB5FF78E202DC~QAAQz1evi8AnnNJmAQAA7NDe5BVIRsAJUZC3BPAt8acPj+aBpSh5cBtX0sPo0cLHHs6fjOsIHY0dX4HWinPtVGMdIpzQOb0dN75sKSsSszzilfWHDE7Cx8rZ5/0PNHEVVCQw4QTLAD231QdTVLjs+jupT+lKysQNjlIIAhS7Y8+a5Oe49154oNULnPRb',
    'ak_bmsc':'D4E7FAF5274A0E4FFA1072BF884E41A48BAF57CFC44A0000947AE05B0C057C1D~plnpIHXksDVvxmjs8ylwPtcWmLK75xmHi/EJQEuvv+tEi/BygrJDgAjXVQPcU9LdeXp0pxo6bhoBR7f7IlECICoEpXtAVEvCObKZNJH/tQ99MhObdhbWLEvs4Jd4BZkmt+vs70oOPqaQMhcFrHYaiPkThXDdX/hTN1BZl+a/umUBMmq+fnp/apJM9DX7F4wUfS93Zgo+dlmq2iLmm4UF6lXOooIzA3fxGgybD3b3HRd70=',
    'bm_mi':'4B54D2638122BB5BEDB097DB10FAD414~IcPPCDqSlsIelbmyfvh1DZYieg8pkiTMaoJFeSRfRQzLXgwfT8j9DO49PomVUMhrYAg5jxZu9FXMlo+t0+3YTrSiabBsm00hg0uMMvQ+g0LmdUgBkJjq6X/kWQzUguZ/J/BGwhR3kqf026QaLtRgiKbHx2ywvTfXZ3e63HhtBYv23cPQ3RLsMLNTdCp4ou2LRXB0NAt8colcIOYYqp8E8kSSoWdsjafjy5/SU/QW3hw=',
    'bm_sv':'0C0DB48FE47F6D1908FDCADCA90D10B3~3oyRYXQguDSiFrZWoRi8QVsoVSkISQWYdOY26Cy/UuoeDjwOCKkfYTd8WnhIBL+x6tOyldlYuNvNpvXNBz3xn/AuM9m/7o+tDmUnW0lVLr3/ztrNkSkH3t+wt3ps1W4TXU4u1+BhKH0OMiBs6DUpHg==',
    'JSESSIONID':'8562CEE10AA61DA99234DE54B92D2408',
    'CC_PORTALID':'1345008',
    'AMOS_OKTOCACHE':'false',
    'COUNTRY_MATCH':'true'
}

headers = {
    'Server':'Apache-Coyote/1.1',
    'Content-Type':'text/html;charset=UTF-8',
    'Content-Language':'zh-TW',
    'Content-Encoding':'gzip',
    'Vary':'Accept-Encoding',
    'Strict-Transport-Security':'max-age=63072000',
    'X-Akamai-Transformed':'9 24850 0 pmb=mTOE,3',
    'Connection':'keep-alive',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://tw.shop.com/',
    'upgrade-insecure-requests': '1'
}

data={
    'st':keyword,
    'sy':'products'
}
url = 'https://tw.shop.com/search/header/'+keyword
res = requests.post(url,data=data,headers=headers,cookies=cookies)
print(res)
#cookies = {"CC_PORTALID":""}

