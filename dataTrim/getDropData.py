import requests
import json


def getDropData(itemId: str, url: str = 'https://penguin-stats.io/PenguinStats/api/v2/result/matrix', fileDir: str = "./db/dropItem.json") -> str:
    '''返回http响应代码'''
    param = {'itemFilter': str(itemId)}
    response = requests.get(url=url, params=param)
    #print(response.url, response.status_code, sep='\n')
    raw_data = json.loads(response.content)
    data = raw_data['matrix']
    with open(fileDir, 'w', encoding='UTF-8') as wr:
        json.dump(data, wr, indent=4)
    return response.status_code

if __name__ == '__main__':
    itemFind=input('需要查询的物品id：')
    