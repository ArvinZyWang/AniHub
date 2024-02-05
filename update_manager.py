from typing import Literal
import utils.scraper as scraper
import json
from datetime import datetime

def load_subscription() -> list[dict]:
    """
    读取./data/subscribed.json, 获取订阅信息。\n
    Returns:
        list[dict]: 订阅信息。
    """
    with open(r'./data/subscribed.json','r', encoding='utf-8') as js:
        data = json.load(js)
    return data

def update_subscription(data):
    """
    将更新后的字典数据载入到磁盘中./data/subscribed.json\n
    Args:
        data (list[dict]): 订阅信息。
    """
    with open(r'./data/subscribed.json','w', encoding='utf-8') as js:
        json.dump(data, js, indent = 4)

def marked_as_watched(anime_index:int, index:int):
    """
    根据选中的订阅动漫的New中的索引数, 判断是否需要更新\n
    Args:
        anime_index (int): 动画
        index (int): New列表中的索引
    """
    data = load_subscription()
    new:list = data[anime_index]['New']
    
    try:
        selected = datetime.fromisoformat(new[index]['pubDate'])
    except:
        selected = datetime.strptime(new[index]['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
    try:
        last_watched_pubdate = datetime.fromisoformat(data[anime_index]['last_watched_pubdate'])
    except:
        last_watched_pubdate = datetime.strptime(data[anime_index]['last_watched_pubdate'], '%a, %d %b %Y %H:%M:%S %z')
            
    if selected > last_watched_pubdate:
        data[anime_index]['last_watched_pubdate'] = str(selected)
        if index < len(data[anime_index]['New']) -1 :
            data[anime_index]['New'] = data[anime_index]['New'][index+1:]
        else:
            data[anime_index]['New'] = []
        update_subscription(data)
    

def check_update():
    """
    检查订阅列表中是否存在更新。\n
    如果遇到更新，将更新条目以{title:'', pubDate:'', magnet:''}的格式载入到订阅列表中的New一栏中。
    """
    animes:list[dict] = load_subscription()
    
    for anime in animes:
        # 跳过已标记为完结的动漫
        if anime['Ended']:
            continue
        # 载入信息
        title = anime['title']
        team = anime['team']
        # 将日期信息转为datetime object
        try:
            last_watched_pubdate = datetime.fromisoformat(anime['last_watched_pubdate'])
        except:
            last_watched_pubdate = datetime.strptime(anime['last_watched_pubdate'], '%a, %d %b %Y %H:%M:%S %z')
        # 搜索
        search_result = scraper.search(title, sort='episode', order='date-desc', team = team)
        
        # 存储搜索结果中所有的图片链接
        imgUrls = anime.get('imgUrls', [])
        for item in search_result:
            imgUrls += item['imgs'] 
        # 去重
        anime['imgUrls'] = list(set(imgUrls))
        
        latest_pubdate = search_result[0]['pubDate']
        
        # 有更新时：
        if latest_pubdate > last_watched_pubdate:
            print(f'{title} 有更新！')
            for index, item in enumerate(search_result):
                if item['pubDate'] <= last_watched_pubdate:
                    # 将所有发布时间晚于上次观看的发布时间的结果，载入到字典中的New一栏中
                    anime['New'] = [{'title':item['title'],
                                     'pubDate':str(item['pubDate']),
                                     'magnet':item['magnet']}
                                    for item in search_result[:index] ]
                    anime['New'].reverse()
                    break
            else:
                # 如果遇上极端情况，字典中存储的上次观看发布时间早于所有搜索结果，就将全部搜索结果载入到字典的New一栏中
                anime['New'] = [{'title':item['title'], 'pubDate':str(item['pubDate']), 'magnet':item['magnet']} for item in search_result ]
                anime['New'].reverse()
        # 无更新时：
        else:
            print(f'{title} 无更新=_=')
            anime['New'] = []
            
    update_subscription(animes)



def subscribe(
            keyword,
            team:Literal['NC-Raws','Lilith-Raws','LoliHouse','北宇治字幕组',
                         'VCB-Studio','桜都字幕组','MingYSub','喵萌奶茶屋','天月動漫&發佈組'] = 'all'):
    """
    添加新的订阅项目。\n
    Args:
        keyword (str): 关键字/动漫标题
        team (str, optional): 发布组, 默认为all。
    """
    animes:list[dict] = load_subscription()
    current_titles = [ item['title'] for item in animes ]
    if keyword in current_titles:
        print('不可重复添加！！')
    else:
        animes.append({'title': keyword, 'team':team,'last_watched_pubdate':'2020-01-01 00:00:00+08:00', 'New':[], "Ended":0})
        update_subscription(animes)

    

if __name__ == '__main__':

    print(None)