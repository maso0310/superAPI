#LineBot Sheet API https://sheetsu.com/apis/v1.0su/7e0b40d2e3f3

# Read whole spreadsheet
from sheetsu import SheetsuClient

client = SheetsuClient("https://sheetsu.com/apis/v1.0su/7e0b40d2e3f3")
print(client.read())
client.create_one(time="測試",message="加入字串")