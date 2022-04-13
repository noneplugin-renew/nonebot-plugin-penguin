from typing import Literal
from tinydb import TinyDB, Query


def queryItemInfo(itemName:str, dbLink='./db/infoIdDB.json'):
    db = TinyDB(dbLink).table('items')
    q = Query()

    itemInfo = {}
    try:
        itemInfo = db.search(q.name == itemName)
        assert itemInfo
    except:
        try:
            itemInfo = db.search(q.alias.any(itemName))
            assert itemInfo
        except:
            itemInfo = '404-NotFound'
    return itemInfo


if __name__ == "__main__":
    itemInfo = queryItemInfo(input("name:"))
    print(itemInfo)
