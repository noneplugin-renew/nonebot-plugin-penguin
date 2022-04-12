from .queryInfo import queryItemInfo
import logging

logging.basicConfig(level=logging.DEBUG,
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
elif len(itemInfoList) > 1:
    logging.debug(f'get itemInfoes:{itemInfoList}')
    print('匹配到多个结果：')
    for itemInfo in itemInfoList:
        print(itemInfo['name'], itemInfo['itemId'], sep=':')
