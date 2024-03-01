import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
root_path = os.path.dirname(lib_path)

sys.path.append(file_path)
sys.path.append(lib_path)

from dataclasses import dataclass, asdict

from models.anime import Anime

@dataclass
class SubscribedAnime:
    title: str = None
    team: str = None
    
    episodes: list[Anime] = None
    
    NewCount: int = 0
    
    imgUrls: list[str] = None
    poster: str = None
    
    def __init__(self, parent, subscription_info:dict) -> None:
        self.parent = parent
        
        self.title = subscription_info.get('title', None)
        self.team = subscription_info.get('team', None)
        
        self.episodes = sorted([Anime(item) for item in subscription_info.get('episodes', [])])
        self.lastWatchedEpisode = None
        for episode in self.episodes[::-1]:
            if episode.watched:
                self.lastWatchedEpisode = episode
                break

        self.NewCount = len([item for item in self.episodes if not item.watched])
        
        self.imgUrls = subscription_info.get('imgUrls', [])
        self.poster = subscription_info.get('poster', None)
        
    def to_dict(self):
        data = asdict(self)
        data['episodes'] = [anime.to_dict() for anime in self.episodes]
        return data
    
    def updateImgUrls(self, imgUrls:list[str] = []):
        for item in self.episodes:
            self.imgUrls += item.imgUrls
        self.imgUrls += imgUrls
        self.imgUrls = list(set(self.imgUrls))
        
    def markAsWatched(self, index:int):
        if not 0 <= index < len(self.episodes):
            raise IndexError("SubscribedAnime.markAsWatched: Index out of range.")
        selected = self.episodes[index]
        if selected.watched:
            return
        self.lastWatchedEpisode = selected
        for anime in self.episodes:
            if anime <= selected:
                anime.watched = True
        self.NewCount = len([item for item in self.episodes if not item.watched])
        self.save()
    
    def markAsUnwatched(self, index:int):
        if not 0 <= index < len(self.episodes):
            raise IndexError("SubscribedAnime.markAsUnwatched: Index out of range.")
        selected = self.episodes[index]
        if not selected.watched:
            return
        for anime in self.episodes:
            if anime >= selected:
                anime.watched = False
        for episode in self.episodes[::-1]:
            if episode.watched:
                self.lastWatchedEpisode = episode
                break
        self.NewCount = len([item for item in self.episodes if not item.watched])
        self.save()
    
    def setPoster(self, img: str):
        self.imgPath = os.path.join(root_path, 'res', self.title)
        self.imgPath = os.path.abspath(self.imgPath)
        
        if not os.path.exists(self.imgPath):
            raise Exception(f'Image folder for {self.title} does not exist.')
        else:
            # 列举出所有文件
            lst = os.listdir(self.imgPath)
            # 如果图片文件存在于列表中，则设置为海报
            if img in lst:
                self.poster = img
                self.save()
                print(f'Poster for {self.title} has been set to {img}')
            else:
                # 如果图片文件不存在于列表中，则抛出异常
                raise Exception(f'Error in setting poster for {self.title}: file {img} doesn\'t exist.')
    
    def edit(self, new_title:str, new_team:str):
        self.imgPath = os.path.join(root_path, 'res', self.title)
        self.imgPath = os.path.abspath(self.imgPath)
        if not os.path.exists(self.imgPath):
            os.makedirs(self.imgPath)
        
        newImgPath = os.path.join(root_path, 'res', new_title)
        os.rename(self.imgPath, newImgPath)
        
        self.title = new_title
        self.team = new_team
        
        self.save()
        
    
    def save(self):
        self.episodes.sort()
        return self.parent.save()
    
if __name__ == '__main__':

    breakpoint()