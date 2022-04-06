import imp
import pandas as pd
import json
import time
from tinydb import TinyDB

stagedb=TinyDB('./src/stageIdDB.json')

def stampToTime(stamp: int) -> str:
    if isinstance(stamp, str):
        return stamp
    local = time.localtime(stamp/1000)
    TimeStr = time.strftime("%Y-%m-%d>%H:%M:%S", local)
    return TimeStr


dropItemDf = pd.read_json('./src/dropItem.json')

# print(dropItemJson.dtypes)
# start列时间戳转换
dropItemDf['start'] = dropItemDf.apply(
    lambda x: stampToTime(x['start']), axis=1)
# 替换end中的NaN
dropItemDf.loc[dropItemDf['end'].isnull(), 'end'] = 'Opening'
# end列时间戳转换
dropItemDf['end'] = dropItemDf.apply(
    lambda x: stampToTime(x['end']), axis=1)
# stageId列替换
dropItemDf['stageId']
# print(dropItemJson.to_string())
print(dropItemDf.head())
