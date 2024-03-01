import sys
import os

from PyQt5.QtGui import QResizeEvent
file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtCore import QEasingCurve, Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame

from qfluentwidgets import SmoothScrollArea

from anime_gallery import AnimeGallery
from lib.subscription import Subscription



class AnimeGalleryScroll(SmoothScrollArea):
    clicked = pyqtSignal(int)
    posterChanged = pyqtSignal(int)
    infoChanged = pyqtSignal(int)
    deleted = pyqtSignal(int)
    cleared = pyqtSignal(int)
    
    def __init__(self, parent, subscription:Subscription):
        super().__init__(parent)
        self.subscription = subscription
        self.update()
        
    def update(self):
        try:
            del self.gallery
        except AttributeError:
            pass
        self.gallery = AnimeGallery(self, self.subscription)
        self.gallery.clicked.connect(self.clicked)
        self.gallery.posterChanged.connect(self.posterChanged)
        self.gallery.infoChanged.connect(self.infoChanged)
        self.gallery.deleted.connect(self.deleted)
        self.gallery.cleared.connect(self.cleared)
        
        self.resizeEvent(None)
            
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFrameStyle(QFrame.NoFrame)
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)
        self.setWidget(self.gallery)
        
        super().update()
        
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        super().resizeEvent(a0)
        if self.gallery.height() < self.height():
            self.gallery.resize(self.width(), self.height())
        self.gallery.setFixedWidth(self.width())