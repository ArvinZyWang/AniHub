from datetime import datetime

def datetimeObj2str(datetimeObj:datetime|None) -> str:
    if isinstance(datetimeObj, datetime):
        return str(datetimeObj)
    else:
        return None

def str2datetimeObj(timeString:str|datetime|None) -> datetime:
    if timeString is None:
        return str2datetimeObj("1970-01-01 00:00:00+08:00")
    
    if type(timeString) == datetime:
        return timeString
    else:
        try:
            datetimeObj = datetime.strptime(timeString, "%a, %d %b %Y %H:%M:%S %z")
        except:
            datetimeObj = datetime.fromisoformat(timeString)
        return datetimeObj
    