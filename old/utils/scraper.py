from typing import Literal
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
import json


def search(
            keyword:str,
            sort:Literal['all','episode','season'] = 'all',
            team:Literal['NC-Raws','Lilith-Raws','LoliHouse','北宇治字幕组','VCB-Studio','桜都字幕组','MingYSub','喵萌奶茶屋','天月動漫&發佈組','亿次研同好会'] = 'all',
            order:Literal['date-desc','date-asc'] = 'date-desc') -> list[dict]:
    """
    根据关键词、分类与排序, 在dmhy.org上搜索。\n
    Args:
        keyword (str): 搜索关键字。
        sort: 全部/单集动画/季度全集，默认为全部。
        order: 搜索顺序，默认按发布时间从后往前。
        team:  发布组，默认为全部。

    Returns:
        list[dict]: 返回结果为列表, 列表元为字典, 包含标题、发布时间、磁力链接与配图链接列表。
    """
    
    # 分类：sort_id=0 -> 全部   sort_id=2 -> 动画   sort_id=31 -> 季度全集
    # 排序: order = date-desc -> 时间从后往前   order = date-asc -> 时间从前往后
    sorts = {'all':0, 'episode':2, 'season':31}
    with open(r'./data/teams.json', "r", encoding='utf-8') as f:
        teams = json.load(f)
        
    url =f'https://www.dmhy.org/topics/rss/rss.xml?keyword={keyword}&sort_id={sorts[sort]}&team_id={teams[team]}&order={order}'
    
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    headers['Host'] = 'www.dmhy.org'
    
    page = requests.get(url = url, headers= headers)
    
    bs = BeautifulSoup(page.text, features='xml')
    
    items = []
    for item in bs.find_all('item'):
        item_dic = {}
        item_dic['title'] = item.find('title').get_text()
        item_dic['pubDate'] = datetime.strptime(item.find('pubDate').get_text(), "%a, %d %b %Y %H:%M:%S %z")
        item_dic['magnet'] = item.find('enclosure')['url']
        try:
            description = item.find('description').get_text()
            imgs = BeautifulSoup(str(description), 'html.parser').find_all('img')
            item_dic['imgs'] = [img['src'] for img in imgs]
        except:
            item['imgs'] = []
        items.append(item_dic)
    
    return items

def download_image(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            image.save(save_path)
            print(f"Image downloaded successfully and saved at: {save_path}")
        else:
            print(f"Failed to download image. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
     

if __name__ == '__main__':
    """result = search('It\'s MyGO', team='LoliHouse')
    imgs = []
    for item in result:
            for key in item:
                imgs += item['imgs']
                print(f'{key} : {item[key]}')
                print('-'*20)
            print('=*'*50)
            
    imgs = list(set(imgs))
    print('\n'*5,imgs)"""
    
    mygo_imgs = ['https://anime.bang-dream.com/mygo/wordpress/wp-content/themes/mygo_v1/assets/images/pc/index/img_kv-1.jpg',
     'https://s2.loli.net/2023/07/01/l92AMea8kdyYDtC.jpg', 
     'https://anime.bang-dream.com/mygo/wordpress/wp-content/themes/mygo_v1/assets/images/pc/index/img_kv-0.jpg']
    
    import os
    current_dir = os.path.dirname(os.path.realpath(__file__))
    mydir = os.path.join(current_dir, 'imgs_test')
    for img in mygo_imgs:
        download_image(img, mydir)