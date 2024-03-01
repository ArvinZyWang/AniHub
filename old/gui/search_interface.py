from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from search_bar import SearchBar
from search_result_table import SearchResult

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
from utils import scraper



class SearchInterface(QWidget):
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.resize(750, 700)
        self.initUI()
        
    def initUI(self):
        self.search_thread = SearchAction()
        self.search_thread.finished.connect(self.on_thread_finished)
        
        self.search_bar = SearchBar(self, [90,50])
        self.search_bar.search_signal.connect(self.search)
        
        self.search_table = SearchResult(self, [90,150])
        self.show()
        
    def search(self,args):
        self.search_thread.set_args(args)
        self.search_bar.SearchLineEdit.setDisabled(True)
        self.search_thread.start()
        
    def on_thread_finished(self):
        self.search_table.result = self.search_thread.result
        self.search_bar.SearchLineEdit.setDisabled(False)
        self.search_table.update()
        
class SearchAction(QThread):
    
    finnished = pyqtSignal(list)
    
    def run(self):
        result = scraper.search(*self.args)
        self.finnished.emit(result)
        self.result = result
        
    def set_args(self, args):
        self.args = args
        
    
    
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    class test(QWidget):
        
        def __init__(self, parent = None) -> None:
            super().__init__(parent)
            self.initUI()
            self.resize(800, 700)
            
        def initUI(self):
            ###
            t = SearchInterface(self)
            t.move(0,0)
            ###
            self.show()
        
    app = QApplication(sys.argv)    
    test_window = test()
    sys.exit(app.exec_())