import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
sys.path.append(lib_path)

from dataclasses import dataclass, asdict

from utils.datetime_covertor import datetime, datetimeObj2str, str2datetimeObj

@dataclass
class Anime:
    
    title: str = None
    magnet: str = None
    
    watched: bool = False
    
    pubDate: datetime = None
    
    imgUrls: list[str] = None
    
    def __init__(self, anime_info:dict | None = None):
        if not anime_info is None:
            self.setInfo(anime_info)
    
    def setInfo(self, anime_info:dict):
        """get an instance of Anime according to the given dict.\n
        dict example:\n
            {
                'title': '__Title__',
                'magnet': '__Magnet__',
                'pubDate': '__Publishing Date__',
                'imgUrls': ['url1', 'url2', 'url3'...]
            }
        """
        self.title = anime_info.get('title', None)
        self.magnet = anime_info.get('magnet', None)
        
        self.watched = anime_info.get('watched', False)
        
        self.pubDate = str2datetimeObj(anime_info.get('pubDate',None))

        self.imgUrls = anime_info.get('imgUrls', [])
        
        return self
    
    def to_dict(self):
        data = asdict(self)
        data['pubDate'] = datetimeObj2str(self.pubDate)
        return data
    
    def __lt__(self, other:'Anime') -> bool:
        if other is None:
            return False
        if isinstance(self, Anime) and isinstance(other, Anime):
            return self.pubDate < other.pubDate
        else:
            raise TypeError('Anime object expected.')
        
    def __gt__(self, other:'Anime') -> bool:
        if other is None:
            return True
        if isinstance(self, Anime) and isinstance(other, Anime):
            return self.pubDate > other.pubDate
        else:
            raise TypeError('Anime object expected.')
        
    def __ge__(self, other:'Anime') -> bool:
        if isinstance(self, Anime) and isinstance(other, Anime):
            return self.pubDate >= other.pubDate
        else:
            raise TypeError('Anime object expected.')
    
    def __le__(self, other:'Anime') -> bool:
        if isinstance(self, Anime) and isinstance(other, Anime):
            return self < other or self.pubDate == other.pubDate
        
