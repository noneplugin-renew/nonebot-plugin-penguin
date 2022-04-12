import pandas
from queryInfo import queryItemInfo
from getDropData import getDropData
from trimDropData import trimDropData, dumpToHMTL
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

itemName = input("需要查询的物品：")
logging.debug(f'get name:{itemName}')
itemInfoList = queryItemInfo(itemName)
logging.debug(f'get itemInfo:{itemInfoList}')

if isinstance(itemInfoList, str):
    print('nothing')
    logging.warning(f'search failed: {itemName} not exist')
elif len(itemInfoList) == 1:
    logging.debug(f'got itemInfo:{itemInfoList}')
    print(itemInfoList[0]['name'], itemInfoList[0]['itemId'], sep=':')
    itemId = itemInfoList[0]['itemId']
elif len(itemInfoList) > 1:
    logging.debug(f'get itemInfoes:{itemInfoList}')
    print('匹配到多个结果：')
    for idx,itemInfo in enumerate(itemInfoList):
        print(idx,itemInfo['name'], itemInfo['itemId'], sep=':')
    idxSelect=int(input('请输入需要的物品序号：'))
    itemId = itemInfoList[idxSelect]['itemId']
    logging.debug(f'get id:{itemId}')

resultGet = getDropData(str(itemId))
logging.debug(f'http statue:{resultGet}')

trimDataList=trimDropData()
for trimData in trimDataList:
    print(trimData.head(8).to_string(columns=['stageName','apCost','frequency','aCPI']))

isToHtml=input('是否输出成HTML(y|n)：')
if isToHtml.upper() == 'Y':
    resultHtml = dumpToHMTL(*trimDataList)