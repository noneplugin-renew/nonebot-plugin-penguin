from pandas import Timestamp
import requests
import json
import time
from tinydb import TinyDB

itemdb = TinyDB('./src/itemIdDB.json')
#先全清空好了，后面再看情况改成逐条修改吧
itemdb.truncate()
# 写入本次更新信息时的时间戳
itemdb.insert({'updateTime': int(time.time())})

url = 'https://penguin-stats.io/PenguinStats/api/v2/items'
urlResponse = requests.get(url)
rawData = json.loads(urlResponse.content)

for item in rawData:
    itemId=item['itemId']
    name=item['name']
    alias=item['alias']
    data={
        'itemId':itemId,
        'name':name,
        'alias':alias
    }
    itemdb.insert(data)