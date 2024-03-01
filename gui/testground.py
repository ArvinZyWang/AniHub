import sys
import os
file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(root_path)

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QWidget

from search_interface.search_bar import SearchBar
from search_interface.search_result_table import SearchResultTable

from gui.subscription_interface.anime_card import AnimeCard
from gui.subscription_interface.anime_gallery import AnimeGallery
from gui.subscription_interface.anime_gallery_scroll import AnimeGalleryScroll
from gui.subscription_interface.interface import SubscriptionInterface
from gui.subscription_interface.anime_episodes_table import AnimeEpisodesTable

class TestWindow(QWidget):
    
    def __init__(self, testWidget) -> None:
        super().__init__()
        self.testWidget = testWidget
        self.setting()
        self.show()
        
    def setting(self):
        from lib.subscription import Subscription
        subscription = Subscription()
        example_list = subscription.data[-1].episodes
        example_anime = subscription.data[0]
        
        if self.testWidget is SearchBar:
            self.testWidget = self.testWidget(self)
            self.testWidget.initUi()
            self.testWidget.searchSignal.connect(lambda args: print(args))
            
        if self.testWidget is SearchResultTable:
            self.testWidget = self.testWidget(self)
            self.testWidget.resize(650, 500)
            self.testWidget.initUi()
            self.testWidget.setData(example_list)
            self.testWidget.update()
            
        if self.testWidget is AnimeCard:
            self.testWidget = self.testWidget(None, example_anime)
            self.testWidget.clicked.connect(lambda: print('Anime card clicked.'))
            self.testWidget.show()
            
        if self.testWidget is AnimeGallery:
            self.testWidget = self.testWidget(None, subscription)
            self.testWidget.clicked.connect(lambda i: print(f'{subscription.data[i].title} is clicked.'))
            
        if self.testWidget is AnimeGalleryScroll:
            self.testWidget = self.testWidget(self, subscription)
            self.testWidget.resize(400, 200)
            self.testWidget.gallery.clicked.connect(lambda i: print(f'{subscription.data[i].title} is clicked.'))
            
        if self.testWidget is SubscriptionInterface:
            self.testWidget = self.testWidget(None)
            self.testWidget.resize(1200,800)
            
        if self.testWidget is AnimeEpisodesTable:
            self.resize(400,500)
            self.testWidget = self.testWidget(self)
            self.testWidget.setData(example_list)
            self.testWidget.resize(700, 300)
            
            
            
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
app = QApplication(sys.argv)
window = TestWindow(SubscriptionInterface)
app.exec_()