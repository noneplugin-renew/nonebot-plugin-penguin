from pandas import Timestamp
import requests
import json
import time
from tinydb import TinyDB

stagedb = TinyDB('./src/stageIdDB.json')
#先全清空好了，后面再看情况改成逐条修改吧
stagedb.truncate()
# 写入本次更新信息时的时间戳
stagedb.insert({'updateTime': int(time.time())})

url = 'https://penguin-stats.io/PenguinStats/api/v2/stages'
urlResponse = requests.get(url)
rawData = json.loads(urlResponse.content)

for stage in rawData:
    stageId = stage['stageId']
    code = stage['code']
    apCost = stage['apCost']
    minClearTime = stage['minClearTime']
    data = {
        'stageId': stageId,
        'code': code,
        'apCost': apCost,
        'minClearTime': minClearTime
    }
    stagedb.insert(data)
