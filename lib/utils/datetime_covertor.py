from datetime import datetime, timedelta, timezone

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
            datetimeObj = datetime.fromisoformat(timeString)
        except ValueError:
            try:
                datetimeObj = datetime.strptime(timeString, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                utc_plus_8 = timezone(timedelta(hours=8))
                datetimeObj = datetime.strptime(timeString, '%a, %d %b %Y %H:%M:%S GMT')
                datetimeObj = datetimeObj.replace(tzinfo=utc_plus_8)
        return datetimeObj
    