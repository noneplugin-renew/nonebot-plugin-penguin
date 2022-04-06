import pandas as pd
import json
import time
from tinydb import TinyDB, Query

stagedb = TinyDB('./db/stageIdDB.json')
stageQuery = Query()


def stampToTime(stamp: int) -> str:
    if isinstance(stamp, str):
        return stamp
    local = time.localtime(stamp/1000)
    TimeStr = time.strftime("%Y.%m.%d>%H:%M", local)
    return TimeStr


def pushStageName(stageId: str) -> str:
    stage = stagedb.search(stageQuery.stageId == stageId)
    return stage[0]['code']


def calFrequency(times: int, quantity: int) -> float:
    return quantity/times


def calaCPI(apCost: int, freq: int) -> float:
    if freq == 0:
        return 0
    return apCost/freq


def pushApCost(stageId: str) -> int:
    stage = stagedb.search(stageQuery.stageId == stageId)
    apCost = stage[0]['apCost']
    return apCost if apCost else 0


dropItemDf = pd.read_json('./db/dropItem.json')

# print(dropItemJson.dtypes)
# start列时间戳转换
dropItemDf.start = dropItemDf.apply(
    lambda x: stampToTime(x.start), axis=1)
# 替换end中的NaN
dropItemDf.loc[dropItemDf.end.isnull(), 'end'] = 'Opening'
# end列时间戳转换
dropItemDf.end = dropItemDf.apply(
    lambda x: stampToTime(x.end), axis=1)
# 在stageId列后添加新列stageName
# 在quantity列后添加新列frequency
columnList1 = dropItemDf.columns.to_list()
columnList1.insert(columnList1.index('quantity')+1, 'frequency')
columnList1.insert(columnList1.index('stageId')+1, 'stageName')
dropItemDf = dropItemDf.reindex(columns=columnList1)
# 写入name
dropItemDf.stageName = dropItemDf.apply(
    lambda x: pushStageName(x.stageId), axis=1
)
# 计算frequency
dropItemDf.frequency = dropItemDf.apply(
    lambda x: calFrequency(x.times, x.quantity), axis=1
)
# 在frequency列后添加新列apCost,aCPI(apCostPerItem,单件期望理智消耗)
columnList2 = dropItemDf.columns.to_list()
columnList2.insert(columnList2.index('stageId')+1, 'apCost')
columnList2.insert(columnList2.index('frequency')+1, 'aCPI')
dropItemDf = dropItemDf.reindex(columns=columnList2)
# 写入apCost数据
dropItemDf.apCost = dropItemDf.apply(
    lambda x: pushApCost(x.stageId), axis=1
)
# 删除补给箱子行(apCost=99)
dropItemDf.drop(dropItemDf[dropItemDf.apCost >= 99].index, inplace=True)
# 删除样本过小的行(times or quantity <10)
dropItemDf.drop(dropItemDf[dropItemDf.times < 10].index, inplace=True)
dropItemDf.drop(dropItemDf[dropItemDf.quantity < 10].index, inplace=True)
# 计算aCPI
dropItemDf.aCPI = dropItemDf.apply(
    lambda x: calaCPI(x.apCost, x.frequency), axis=1
)
# 按frequency,aCPI排序并重置索引
dropItemDfByFreq = dropItemDf.sort_values(by='frequency', ascending=False)
dropItemDfByaCPI = dropItemDf.sort_values(by='aCPI', ascending=True)
dropItemDfByFreq.reset_index(drop=True, inplace=True)
dropItemDfByaCPI.reset_index(drop=True, inplace=True)
print(dropItemDfByaCPI.head())
print(dropItemDfByFreq.head())
