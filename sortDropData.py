import pandas as pd
import json,time

def stampToTime(stamp:int) -> str:
    if isinstance(stamp,str):
        return stamp
    local=time.localtime(stamp/1000)
    TimeStr=time.strftime("%Y-%m-%d>%H:%M:%S",local)
    return TimeStr


dropItemJson=pd.read_json('./src/dropItem.json')
print(dropItemJson.dtypes)
dropItemJson['start'] = dropItemJson.apply(lambda x :stampToTime(x['start']),axis=1)
dropItemJson = dropItemJson.fillna(value='Opening')
dropItemJson['end'] = dropItemJson.apply(lambda x :stampToTime(x['end']),axis=1)
print(dropItemJson.to_string())
