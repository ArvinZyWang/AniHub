import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)

sys.path.append(file_path)
sys.path.append(lib_path)

from typing import Literal
import requests
from urllib.parse import quote

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from models.anime import Anime
from models.server import Server
from models.settings import Settings
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
            setting = Settings()
            result = self.__get_result(setting.server, *self.args)
            self.finished.emit(result)
            del setting
        else:
            raise Exception('Search called, but no args were given.')
    
    @staticmethod
    @cache(enable= True, timeout = 60)
    def __get_result(server:str,
                     keyword:str,
                     sort:Literal['all','episode','season'] = 'all',
                     team = 'all') -> list[Anime]:
        # 分类：sort_id=0 -> 全部   sort_id=2 -> 动画   sort_id=31 -> 季度全集

        try:
            response = Search.__get_response(server, keyword, sort, team)
            if response.status_code == 200:
                print(f'Succeeded in searching for {keyword} from {server}.')
            else:
                print(f"Failed to search {keyword} from {server}. HTTP Status Code: {response.status_code}.")
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                print(f"Time out: Failed to search {keyword} from {server}")
                return None
        except Exception as e:
            print(f'Failed to search {keyword} from {server}. Error: {e}')
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
            result.append(Anime.new(temp_dict))
        return result
    
    @staticmethod
    def __get_response(server:str,
                    keyword:str,
                    sort:Literal['all','episode','season'] = 'all',
                    team = 'all') -> requests.Response:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        match server:
            
            
            case Server.MAIN.value:
                team_id = teams[team]
                match sort:
                    case 'all':
                        sort_id = 0
                    case 'episode':
                        sort_id = 2
                    case 'season':
                        sort_id = 31
                        
                headers['Host'] = 'www.dmhy.org'
                
                url =f'https://www.dmhy.org/topics/rss/rss.xml?keyword={keyword}&sort_id={sort_id}&team_id={team_id}'
                response = requests.get(url = url, headers= headers, timeout=5)
                return response
            
            case Server.WAAA.value:
                team_id = teams[team]
                match sort:
                    case 'all':
                        sort_id = 0
                    case 'episode':
                        sort_id = 2
                    case 'season':
                        sort_id = 31
                        
                url =f'https://dmhy.waaa.moe/topics/rss/rss.xml?keyword={keyword}&sort_id={sort_id}&team_id={team_id}'
                response = requests.get(url = url, headers= headers, timeout=5)
                return response
            
            case Server.ONEKUMA.value:
                filter = {'search': keyword, 'fansubId':None, 'type':None}
                
                filter['search'] = keyword
                
                team_id = teams[team]
                if team_id != 0:
                    filter["fansubId"] = team_id
                    
                match sort:
                    case 'all':
                        pass
                    case 'episode':
                        filter["type"] = '動畫'
                    case 'season':
                        filter["type"] = '季度全集'

                if filter['fansubId'] and filter['type']:
                    url = f'https://garden.onekuma.cn/feed.xml?filter=%5B%7B%22fansubId%22:%5B%22{filter["fansubId"]}%22%5D,%22type%22:%22{quote(filter["type"])}%22,%22search%22:%5B%22{quote(filter["search"])}%22%5D%7D%5D'
                elif filter['fansubId']:
                    url = f'https://garden.onekuma.cn/feed.xml?filter=%5B%7B%22fansubId%22:%5B%22{filter["fansubId"]}%22%5D,%22search%22:%5B%22{quote(filter["search"])}%22%5D%7D%5D'
                elif filter['type']:
                    url = f'https://garden.onekuma.cn/feed.xml?filter=%5B%7B%22type%22:%22{quote(filter["type"])}%22,%22search%22:%5B%22{quote(filter["search"])}%22%5D%7D%5D'
                else:
                    url = f'https://garden.onekuma.cn/feed.xml?filter=%5B%7B%22search%22:%5B%22{quote(filter["search"])}%22%5D%7D%5D'

                headers['Host'] = 'garden.onekuma.cn'
                headers['Sec-Ch-Ua-Platform'] = "Windows"
                headers['Sec-Fetch-Dest'] = 'document'
                response = requests.get(url = url, headers= headers, timeout=5)
                return response
                
                
    
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
    #breakpoint()
    search("It's mygo")
    app.exec_()