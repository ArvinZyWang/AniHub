import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)

sys.path.append(file_path)
sys.path.append(lib_path)

from PyQt5.QtCore import pyqtSignal, QThread, QEventLoop

from models.anime import Anime
from models.subscribed_anime import SubscribedAnime
from crawler.search import Search

class Update(QThread):
    
    finished = pyqtSignal()
    
    def __init__(self, anime:SubscribedAnime) -> None:
        super().__init__()
        self.anime = anime
        
    def run(self):
        self.search = Search(keyword = self.anime.title, team = self.anime.team, sort = 'episode')
        self.search.finished.connect(lambda result:self.__onSearchFinished(result))
        self.search.start()
        # 建立EventLoop，防止线程终止，等待结束信号，结束信号将终止这个EventLoop
        loop = QEventLoop()
        self.search.finished.connect(loop.quit)
        loop.exec_()
        
    def __onSearchFinished(self, search_result:list[Anime]):
        newCount = 0
        # 确保self.anime.episodes是一个列表
        if not self.anime.episodes:
            self.anime.episodes = []
    
        # 获取当前所有episodes的唯一标识符集合，假设使用title作为唯一标识符
        currentEpisodesTitles = {episode.title for episode in self.anime.episodes}
    
        for item in search_result:
            # 检查新搜索结果的episode是否已存在于当前列表中
            if item.title not in currentEpisodesTitles:
                self.anime.episodes.append(item)
                newCount += 1
                currentEpisodesTitles.add(item.title)  # 更新集合以包含新添加的episode
        if newCount <= 0:
            print(f'No updates found for {self.anime.title}.')
        else:
            print(f'Found {newCount} new updates for {self.anime.title}.')
            self.anime.updateImgUrls()
            self.anime.save()
        self.finished.emit()
        self.search.quit()
    
    def __repr__(self) -> str:
        return f"Thread for updating {self.anime.title}"
            
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    from subscription import Subscription
    
    subscription = Subscription()
    #subscription.add("It's MyGo", "LoliHouse")
    app = QApplication(sys.argv)
    update = Update(subscription.data[-1])
    update.finished.connect(lambda: print('Update completed.'))
    update.start()
    app.exec_()