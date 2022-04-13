from typing import Literal
from pandas import Timestamp
import requests
import json
import time
from tinydb import Query, TinyDB


def updateItemInfo(updateType: Literal['items', 'stages', 'all'], dbLink: str = './db/infoIdDB.json', url: str = 'https://penguin-stats.io/PenguinStats/api/v2/') -> tuple[str, int]:
    '''
    - 用于更新itemId或者stageId数据库的信息，有默认形参如上
    - 返回值：(更新状态，更新时间戳)
    '''
    try:
        infodb = TinyDB(dbLink, indent=4)
        if updateType == 'items' or updateType == 'all':
            itemdb = infodb.table('items')
            updateTime = int(time.time())

            urlResponse = requests.get(url+'items')
            rawData = json.loads(urlResponse.content)
            assert rawData, 'update Failed: request Empty'

            # 先全清空好了，后面再看情况改成逐条修改吧
            itemdb.truncate()
            # 写入本次更新信息时的时间戳
            itemdb.insert({'updateTime': updateTime})

            for item in rawData:
                itemId = item['itemId']
                name = item['name']
                alias = item['alias']['zh']
                data = {
                    'itemId': itemId,
                    'name': name,
                    'alias': alias
                }
                itemdb.insert(data)

        if updateType == 'stages' or updateType == 'all':
            stagedb = infodb.table('stages')
            updateTime = int(time.time())

            urlResponse = requests.get(url+'stages')
            rawData = json.loads(urlResponse.content)
            assert rawData, 'update Failed: request Empty'

            # 先全清空好了，后面再看情况改成逐条修改吧
            stagedb.truncate()
            # 写入本次更新信息时的时间戳
            stagedb.insert({'updateTime': updateTime})

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
    except Exception as e:
        return repr(e), updateTime
    else:
        return 'OK', updateTime


def updateCheck(dbLink: str = './db/infoIdDB.json') -> dict:
    '''检测itemId和stageId数据库是否需要更新 返回diffSeconds['item','stage']'''
    infodb = TinyDB(dbLink, indent=4)
    itemdb=infodb.table('items')
    stagedb=infodb.table('stages')
    itemdbLastUpdateTime=itemdb.search(Query().updateTime.exists())[0]['updateTime']
    stagedbLastUpdateTime=stagedb.search(Query().updateTime.exists())[0]['updateTime']
    nowTime=int(time.time())
    diffSeconds = {
        'item':(nowTime - int(itemdbLastUpdateTime)),
        'stage':(nowTime - int(stagedbLastUpdateTime))
        }
    return diffSeconds


if __name__ == '__main__':
    '''
    result, updatetime = updateItemInfo('items')
    print(result, updatetime, sep='\n')
    result, updatetime = updateItemInfo('stages')
    print(result, updatetime, sep='\n')
    '''
    id=int(input('id:'))
    if id == 1:
        result, updatetime = updateItemInfo('all')
        print(result, updatetime, sep='\n')
    elif id == 2:
        diff=updateCheck()
        temp = time.ctime(diff['item'])
        diffHours=round(diff['item']/(60*60),3)
        print(f'{diffHours}hour')
