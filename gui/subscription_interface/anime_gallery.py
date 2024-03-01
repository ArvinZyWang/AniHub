import sys
import os
file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEasingCurve, pyqtSignal

from qfluentwidgets import FlowLayout

from anime_card import AnimeCard
from lib.subscription import Subscription

class AnimeGallery(QWidget):
    clicked = pyqtSignal(int)
    posterChanged = pyqtSignal(int)
    infoChanged = pyqtSignal(int)
    deleted = pyqtSignal(int)
    cleared = pyqtSignal(int)
    
    item_width = 150
    item_height = int(item_width * 2**0.5)
    
    
    def __init__(self, parent, subscription: Subscription) -> None:
        super().__init__(parent)
        self.subscription = subscription
        self.resize(600, self.item_height*(len(self.subscription.data)+1)//2)
        self.initUi()
        self.show()
        
        
    def initUi(self):
        self.flowlayout = FlowLayout(self, needAni = True)
        self.flowlayout.setAnimation(250, QEasingCurve.OutQuad)
        self.flowlayout.setContentsMargins(30, 30, 30, 30)
        self.flowlayout.setVerticalSpacing(20)
        self.flowlayout.setHorizontalSpacing(10)
        self.update()
        
    def update(self):
        for index, anime in enumerate(self.subscription.data):
            anime = AnimeCard(self, anime)
            anime.setFixedSize(self.item_width, self.item_height)
            
            anime.clicked.connect(lambda i = index: self.clicked.emit(i))
            anime.posterChanged.connect(lambda i = index: self.posterChanged.emit(i))
            anime.infoChanged.connect(lambda i = index: self.infoChanged.emit(i))
            anime.deleted.connect(lambda i = index: self.deleted.emit(i))
            anime.cleared.connect(lambda i = index: self.cleared.emit(i))
            
            self.flowlayout.addWidget(anime)
        super().update()
