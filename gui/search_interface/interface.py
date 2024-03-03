import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtWidgets import QWidget, QGridLayout

from search_bar import SearchBar
from search_result_table import SearchResultTable

from lib.crawler.search import Search

class SearchInterface(QWidget):
    # 可以考虑用Hbox重写布局
    def __init__(self, parent: QWidget | None) -> None:
        
        # Init UI
        super().__init__(parent)
        
        self.resize(650, 700)
        
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(30,45,30,30)
        self.setLayout(self.grid)
        
        self.search_bar = SearchBar(self)
        self.search_bar.searchSignal.connect(self.__searchThread)
        self.grid.addWidget(self.search_bar, 0, 0, 2, 5)
        self.search_bar.initUi()
        
        self.Table = SearchResultTable(self)
        self.grid.addWidget(self.Table, 2, 0, 11, 9)
        self.Table.initUi()
        
        self.show()
    
    def setEnabled(self, a0: bool) -> None:
        return super().setEnabled(a0)
    
    def __searchThread(self, args:list[str]):
        # Set Search Thread
        self.setEnabled(False)
        self.search_thread = Search(*args)
        self.search_thread.finished.connect(lambda data: self.Table.setData(data))
        self.search_thread.finished.connect(self.Table.update)
        self.search_thread.finished.connect(lambda data:print(data))
        self.search_thread.finished.connect(lambda data: self.setEnabled(True))
        self.search_thread.start()
        
    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        print(f'Current Size: width = {self.width()}, height = {self.height()}')
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    interface = SearchInterface(None)
    app.exec_()
    