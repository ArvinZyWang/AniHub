import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
sys.path.append(lib_path)

from dataclasses import dataclass, asdict, field

from utils.datetime_covertor import datetime, datetimeObj2str, str2datetimeObj

@dataclass
class Anime:
    
    title: str = None
    magnet: str = None
    
    watched: bool = False
    
    pubDate: datetime = None
    
    imgUrls: list[str] = field(default_factory=list)
    
    @classmethod
    def new(cls, info:dict):
        self =cls.__new__(cls)
        self.__init__()
        for key in info:
            if hasattr(self, key):
                setattr(self, key, info[key])
        self.pubDate = str2datetimeObj(self.pubDate)
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
        
