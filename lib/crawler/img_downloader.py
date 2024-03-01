import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
root_path = os.path.dirname(lib_path)
res_path = os.path.join(root_path, 'res')

sys.path.append(file_path)
sys.path.append(lib_path)

import requests
from io import BytesIO
from PIL import Image

from PyQt5.QtCore import pyqtSignal, QThread

from models.subscribed_anime import SubscribedAnime

class DownloadPoster(QThread):
    finished = pyqtSignal()
    
    def __init__(self, anime:SubscribedAnime) -> None:
        super().__init__()
        
        self.anime = anime
        self.imgUrls = anime.imgUrls
        
        self.imgPath = os.path.join('.', 'res', self.anime.title)
        self.imgPath = os.path.abspath(self.imgPath)
        
        if not os.path.exists(self.imgPath):
            os.makedirs(self.imgPath)
        
        self.targetImgNames = [url.split("/")[-1] for url in self.imgUrls]
        
    def run(self):
        for url, filename in zip(self.imgUrls, self.targetImgNames):
            savePath = os.path.join(self.imgPath, filename)
            if os.path.exists(savePath):
                if self.anime.poster is None:
                    self.anime.poster = filename
                    self.anime.save()
                continue
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    image = Image.open(image_data)
                    image.save(savePath)
                    print(f"Image downloaded successfully and saved at: {savePath}")
                    if self.anime.poster is None:
                        self.anime.poster = filename
                        self.anime.save()
                else:
                    print(f"Failed to download poster for {self.anime.title}. HTTP Status Code: {response.status_code}")
            except Exception as e:
                print(f"Error in downloading poster for {self.anime.title}: {e}")
        self.finished.emit()
        
    def __repr__(self):
        return f"Thread for downloading poster for {self.anime.title}"

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from subscription import Subscription
    
    subscription = Subscription()
    app = QApplication(sys.argv)
    thread = DownloadPoster(subscription.data[-1])
    thread.start()
    thread.finished.connect(lambda: print('Poster downloading completed.'))
    app.exec_()