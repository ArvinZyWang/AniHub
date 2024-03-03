import time
import requests

from PyQt5.QtCore import QEventLoop, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
import sys

def ping(url:str) -> tuple[str,int]:
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    try:
        print(f'Start to ping {url}.')
        start_time = time.time()  # 记录发送请求的时间
        response = requests.get(url, headers=headers, timeout=5)  # 发送GET请求
        end_time = time.time()  # 记录收到响应的时间
        latency = int((end_time - start_time) * 1000) # 计算延迟，并转换为毫秒
        print(f'Lantency for {url}: {latency} ms')
    except requests.RequestException as e:
        latency = -1  # 如果请求失败，将延迟设置为-1
        print(f'Unable to fetch {url}, Error: {e}')
    return (url, latency)
        
def pingUrls(urls:list[str]) -> list[tuple[str,int]]:
    result = []
    
    def callback(r:list[tuple[str,int]]):
        nonlocal result
        r.sort(key=lambda item: 50000 if item[1] == -1 else item[1])
        result = r
        app.quit()
        return r
    app = QApplication(sys.argv)
    
    thread = PingMultithread(urls)
    thread.finished.connect(lambda r: callback(r) )
    thread.start()
    app.exec_()
    
    return result
    

class Ping(QThread):
    finished = pyqtSignal(tuple)
    done = False
    
    def __init__(self, url:str):
        super().__init__()
        self.url = url

    def run(self):
        result = ping(self.url)
        self.done =True
        self.finished.emit(result)
    
    def __repr__(self) -> str:
        return f"Ping for {self.url}"
    
class PingMultithread(QThread):
    result:list[tuple[str,int]] = []
    loop: QEventLoop = None
    finished = pyqtSignal(list)
    
    def __init__(self, urls:list[str]) -> None:
        self.urls = urls
        self.threads = [Ping(url) for url in self.urls]
        for thread in self.threads:
            thread.finished.connect(lambda result: self.onThreadFinished(result))
        super().__init__()
        
    def onThreadFinished(self, r):
        self.result.append(r)
        if all(thead.done for thead in self.threads):
            self.finished.emit(self.result)
            if self.loop:
                self.loop.quit()
        
    
    def run(self):
        self.loop = QEventLoop()
        for thread in self.threads:
            thread.start()
        self.loop.exec_()
    
    def __repr__(self) -> str:
        return f"Multithread to ping urls."

    
if __name__ =="__main__":
    urls = [
        'https://www.baidu.com',
        'https://www.google.com',
        'https://www.bilibili.com'
    ]
    print(pingUrls(urls))