from tinydb import TinyDB,Query

db=TinyDB('./db/itemIdDB.json')
q=Query()

item=input('需要搜素的物品：')
itemInfo=db.search(q.name == item)
print(itemInfo)