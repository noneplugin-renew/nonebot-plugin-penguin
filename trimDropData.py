import time

import pandas as pd
from tinydb import Query, TinyDB


def _stampToTime(stamp: int) -> str:
    if isinstance(stamp, str):
        return stamp
    local = time.localtime(stamp/1000)
    TimeStr = time.strftime("%Y.%m.%d>%H:%M", local)
    return TimeStr


def _pushStageName(stagedb, stageQuery, stageId: str) -> str:
    stage = stagedb.search(stageQuery.stageId == stageId)
    if stageId[-3:] == 'erm':
        return stage[0]['code']+'·常驻'
    elif stageId[-3:] == 'rep':
        return stage[0]['code']+'·复刻'
    else:
        return stage[0]['code']


def _calFrequency(times: int, quantity: int) -> float:
    return quantity/times


def _calaCPI(apCost: int, freq: int) -> float:
    if freq == 0:
        return 0
    return apCost/freq


def _pushApCost(stagedb, stageQuery, stageId: str) -> int:
    stageQuery = Query()
    stage = stagedb.search(stageQuery.stageId == stageId)
    apCost = stage[0]['apCost']
    return apCost if apCost else 0


def _freqStr(freq: float) -> str:
    freqstr = str(freq*100)
    return f'{freqstr[:6]}%'


def _renameHTMLColumn(dropItemDf: pd.DataFrame, renameDict: dict) -> pd.DataFrame:
    dropItemDfToHTML = dropItemDf.copy()
    dropItemDfToHTML.frequency = dropItemDfToHTML.apply(
        lambda x: _freqStr(x.frequency), axis=1
    )
    dropItemDfToHTML.aCPI = dropItemDfToHTML.apply(
        lambda x: round(x.aCPI, 3), axis=1
    )
    dropItemDfToHTML.rename(columns=renameDict, inplace=True)
    return dropItemDfToHTML


def trimDropData(dbLink: str = './db/infoIdDB.json', jsonLink: str = './db/dropItem.json') -> tuple[pd.DataFrame, pd.DataFrame]:
    '''返回元组(dfByFrep,dfByaCPI)'''
    stagedb = TinyDB(dbLink).table('stages')
    stageQuery = Query()
    dropItemDf = pd.read_json(jsonLink)

    # print(dropItemJson.dtypes)
    # start列时间戳转换
    dropItemDf.start = dropItemDf.apply(
        lambda x: _stampToTime(x.start), axis=1)
    # 替换end中的NaN
    dropItemDf.loc[dropItemDf.end.isnull(), 'end'] = 'Opening'
    # end列时间戳转换
    dropItemDf.end = dropItemDf.apply(
        lambda x: _stampToTime(x.end), axis=1)
    # 在stageId列后添加新列stageName
    # 在quantity列后添加新列frequency
    addColumnList1 = dropItemDf.columns.to_list()
    addColumnList1.insert(addColumnList1.index('quantity')+1, 'frequency')
    addColumnList1.insert(addColumnList1.index('stageId')+1, 'stageName')
    dropItemDf = dropItemDf.reindex(columns=addColumnList1)
    # 写入stageName
    dropItemDf.stageName = dropItemDf.apply(
        lambda x: _pushStageName(stagedb, stageQuery, x.stageId), axis=1
    )
    # 计算frequency
    dropItemDf.frequency = dropItemDf.apply(
        lambda x: _calFrequency(x.times, x.quantity), axis=1
    )
    # 在frequency列后添加新列apCost,aCPI(apCostPerItem,单件期望理智消耗)
    addColumnList2 = dropItemDf.columns.to_list()
    addColumnList2.insert(addColumnList2.index('stageId')+1, 'apCost')
    addColumnList2.insert(addColumnList2.index('frequency')+1, 'aCPI')
    dropItemDf = dropItemDf.reindex(columns=addColumnList2)
    # 写入apCost数据
    dropItemDf.apCost = dropItemDf.apply(
        lambda x: _pushApCost(stagedb, stageQuery, x.stageId), axis=1
    )
    # 删除补给箱子行(apCost=99)
    dropItemDf.drop(dropItemDf[dropItemDf.apCost >= 99].index, inplace=True)
    # 删除样本过小的行(times or quantity <10)
    dropItemDf.drop(dropItemDf[dropItemDf.times < 10].index, inplace=True)
    dropItemDf.drop(dropItemDf[dropItemDf.quantity < 10].index, inplace=True)
    # 计算aCPI
    dropItemDf.aCPI = dropItemDf.apply(
        lambda x: _calaCPI(x.apCost, x.frequency), axis=1
    )
    # 按frequency,aCPI排序并重置索引
    dropItemDfByFreq = dropItemDf.sort_values(by='frequency', ascending=False)
    dropItemDfByaCPI = dropItemDf.sort_values(by='aCPI', ascending=True)
    dropItemDfByFreq.reset_index(drop=True, inplace=True)
    dropItemDfByaCPI.reset_index(drop=True, inplace=True)
    return dropItemDfByFreq, dropItemDfByaCPI


# 生成输出到html文件的dataframe
def dumpToHMTL(dropItemDfByFreq: pd.DataFrame, dropItemDfByaCPI: pd.DataFrame, dbLink: str = './db/infoIdDB.json') -> str:
    try:
        renameDictByFreq = {'stageName': '关卡', 'apCost': '理智',
                            'frequency': '掉率\u2191', 'aCPI': '单件期望理智'}
        renameDictByaCPI = {'stageName': '关卡', 'apCost': '理智',
                            'frequency': '掉率', 'aCPI': '单件期望理智\u2193'}
        HTMLColumnByFreq = ['关卡', '理智', '掉率\u2191', '单件期望理智']
        HTMLColumnByaCPI = ['关卡', '理智', '掉率', '单件期望理智\u2193']

        itemdb = TinyDB(dbLink).table('items')
        itemQuery = Query()
        id_find = dropItemDfByFreq.at[0, 'itemId']
        itemName = itemdb.search(itemQuery.itemId == str(id_find))[0]['name']
        dropItemDfToHTMLByaCPI = _renameHTMLColumn(
            dropItemDfByaCPI, renameDictByaCPI)

        dropItemDfToHTMLByFreq = _renameHTMLColumn(
            dropItemDfByFreq, renameDictByFreq)

        with open('./html/test.html', 'w', encoding='utf-8') as htmlfile:
            print('<!DOCTYPE html>\
            <html>\
            <head>\
                <meta charset="utf-8">\
                <title>企鹅物流数据查询</title>\
                <link rel="stylesheet" type="text/css" href="styles.css">\
            </head>\
            <body>\
            <div>', file=htmlfile)
            print(f'<h3 id="item-name">{itemName}</h3>', file=htmlfile)
            print(dropItemDfToHTMLByaCPI.head(8).to_html(
                columns=HTMLColumnByaCPI, index=False), file=htmlfile)
            print(dropItemDfToHTMLByFreq.head(8).to_html(
                columns=HTMLColumnByFreq, index=False), file=htmlfile)
            print('</div>\
            </body>\
            </html>', file=htmlfile)
    except Exception as e:
        return repr(e)
    else:
        return 'OK'


if __name__ == "__main__":
    result = dumpToHMTL(*trimDropData())
    print(result)
