import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)

sys.path.append(file_path)
sys.path.append(lib_path)

from typing import Literal
import requests

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from models.anime import Anime
from models.team import teams
from utils.cache import cache

class Search(QThread):
    """用以搜索的线程
    搜索结果用funished信号传出
    """
    finished = pyqtSignal(list)
    args = None
    
    def __init__(self, keyword:str,
                 sort: Literal['all','episode','season'] = 'all',
                 team: str = 'all') -> None:
        self.args = (keyword, sort, team)
        super().__init__()
    
    def run(self):
        if not self.args is None:
            result = self.__get_result(*self.args)
            if result:
                self.finished.emit(result)
        else:
            raise Exception('Search called, but no args were given.')
    
    @staticmethod
    @cache(enable= True, timeout = 60)
    def __get_result(keyword:str,
                     sort:Literal['all','episode','season'] = 'all',
                     team = 'all') -> list[Anime]:
        # 分类：sort_id=0 -> 全部   sort_id=2 -> 动画   sort_id=31 -> 季度全集
        # 通过关键字组织url
        team_id = teams[team]
        match sort:
            case 'all':
                sort_id = 0
            case 'episode':
                sort_id = 2
            case 'season':
                sort_id = 31
        print(f'Searching for {keyword}.')
              
        url =f'https://www.dmhy.org/topics/rss/rss.xml?keyword={keyword}&sort_id={sort_id}&team_id={team_id}'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        headers['Host'] = 'www.dmhy.org'
        
        # 获取页面
        try:
            response = requests.get(url = url, headers= headers, timeout=15)
            if response.status_code == 200:
                print(f'Succeeded in searching for {keyword}.')
            else:
                print(f"Failed to search {keyword}. HTTP Status Code: {response.status_code}")
                return None
        except requests.exceptions.ConnectTimeout:
            print(f'Timeout, please consider using proxy.')
        except Exception as e:
            print(f'Failed to search {keyword}. Error:{e}')
            return None
        
        # 利用bs与lxml解析页面，整理为字典，并创建Anime对象
        bs = BeautifulSoup(response.text, features='xml')
        
        result:list = []
        for item in bs.find_all('item'):
            item: BeautifulSoup
            temp_dict = {}
            temp_dict['title'] = item.find('title').get_text()
            temp_dict['pubDate'] = item.find('pubDate').get_text()
            temp_dict['magnet'] = item.find('enclosure')['url']
            try:
                description = item.find('description').get_text()
                imgs = BeautifulSoup(str(description), 'html.parser').find_all('img')
                temp_dict['imgUrls'] = [img['src'] for img in imgs]
            except:
                item['imgUrls'] = []
            result.append(Anime(temp_dict))
            
        return result

    
if __name__ == '__main__':
    import sys
    from PyQt5.QtCore import QEventLoop
    from utils.timer import timer
    def print_result(result:list[Anime]):
        import json
        for item in result:
            print(json.dumps(item.to_dict(), indent=4))
    
    @timer
    def search(keyword:str):
        qthread = Search(keyword, team = "LoliHouse")
        qthread.start()
        loop = QEventLoop()
        qthread.finished.connect(lambda result: print_result(result[:10]))
        qthread.finished.connect(loop.quit)
        loop.exec_()
        
    app = QApplication(sys.argv)
    breakpoint()
    search("It's mygo")
    app.exec_()