import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
root_path = os.path.dirname(lib_path)
res_path = os.path.join(root_path, 'res')

sys.path.append(file_path)
sys.path.append(lib_path)

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QRunnable, QThreadPool, QEventLoop

from img_downloader import DownloadPoster
from subscription import Subscription, SubscribedAnime

class Worker(QRunnable):
    """执行单个更新的Qrunnable对象
    改写自Update类, 为了配合QThreadPool
    """
    thread: DownloadPoster
    
    def __init__(self, anime:SubscribedAnime):
        super().__init__()
        self.anime = anime
        self.thread = DownloadPoster(self.anime)

    @pyqtSlot()
    def run(self):
        self.thread.start()
        # 建立EventLoop，防止线程终止，等待结束信号，结束信号将终止这个EventLoop
        loop = QEventLoop()
        self.thread.finished.connect(loop.quit)
        loop.exec_()
        
    
    def __repr__(self) -> str:
        return f"Poster downloading executor for {self.anime.title}"
    
class PosterDownloaderMultithread(QThread):
    """多线程更新Anime Posters的线程"""
    finished = pyqtSignal()
    workers: list[Worker]
    
    def __init__(self, subscription:Subscription) -> None:
        self.subscription = subscription
        self.workers = [Worker(item) for item in subscription.data]
        for worker in self.workers:
            worker.thread.finished.connect(lambda title = worker.anime.title: print(f"Succeded in downloading posters for {title}"))
        super().__init__()
     
    def run(self):
        pool = QThreadPool.globalInstance()
        for worker in self.workers:
            pool.start(worker)
        # 线程池中的全部线程执行完毕后，释放finished信号
        pool.waitForDone()
        self.finished.emit()
    
    def __repr__(self) -> str:
        return f"Multithread to download posters for the whole subscription."
    
if __name__ =="__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    subscription = Subscription()
    multithreading = PosterDownloaderMultithread(subscription)
    multithreading.start()
    multithreading.finished.connect(lambda: print('All posters are updated.'))
    app.exec_()