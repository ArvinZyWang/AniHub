from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import SearchLineEdit, ComboBox
import json

class SearchBar(QWidget):
    
    search_signal = pyqtSignal(list)
    
    def __init__(self, parent, pos:list[int]) -> None:
        super().__init__(parent)
        self.initUi()
        self.resize(300, 75)
        if not parent is None:
            self.move(*pos)
    
    def initUi(self):
        self.SearchLineEdit = SearchLineEdit(self)
        self.SearchLineEdit.setPlaceholderText('输入番剧标题')
        self.SearchLineEdit.setGeometry(0, 0, 300, 33)
        self.SearchLineEdit.returnPressed.connect(self.SearchLineEdit.search)
        self.SearchLineEdit.searchSignal.connect(self.search_args)
        
        self.ComboBox_Sort = ComboBox(self)
        self.ComboBox_Sort.addItem(' ')
        self.ComboBox_Sort.addItem('单集动画')
        self.ComboBox_Sort.addItem('季度全集')
        self.ComboBox_Sort.setGeometry(0, 40, 100, 32)
        
        self.ComboBox_Team = ComboBox(self)
        self.ComboBox_Team.addItem(' ')
        with open(r'./data/teams.json', "r", encoding='utf-8') as f:
            self.teams = json.load(f)
            team_names = [key for key in self.teams][1:]
        self.ComboBox_Team.addItems(team_names)
        self.ComboBox_Team.setGeometry(110, 40, 150, 32)
        
    def search_args(self):
        args = ['','','']
        args[0] = self.SearchLineEdit.text()
        
        match self.ComboBox_Sort.text():
            case ' ':
                args[1] = 'all'
            case '单集动画':
                args[1] = 'episode'
            case '季度全集':
                args[1] = 'season'
        
        args[2] = 'all' if self.ComboBox_Team.text() == ' ' else self.ComboBox_Team.text()
        
        self.search_signal.emit(args)
        
    

        
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    class test(QWidget):
        
        def __init__(self, parent = None) -> None:
            super().__init__(parent)
            self.resize(500, 500)
            self.initUI()
            
        def initUI(self):
            ###
            t = SearchBar(self, [0,0])
            ###
            self.show()
        
    app = QApplication(sys.argv)    
    test_window = test()
    sys.exit(app.exec_())