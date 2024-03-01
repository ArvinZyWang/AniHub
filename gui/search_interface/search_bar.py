import sys
import os
file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(root_path)

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal

from qfluentwidgets import SearchLineEdit, ComboBox


from lib.models.team import teams

class SearchBar(QWidget):
    
    searchSignal = pyqtSignal(list)
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
    
    def initUi(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.SearchLineEdit = SearchLineEdit(self)
        self.SearchLineEdit.setPlaceholderText('Title')
        self.grid.addWidget(self.SearchLineEdit, 0, 0, 1, 5)
        self.SearchLineEdit.returnPressed.connect(self.SearchLineEdit.search)
        self.SearchLineEdit.searchSignal.connect(self.emitArgs)
        
        self.ComboBoxSort = ComboBox(self)
        self.ComboBoxSort.addItem('全部')
        self.ComboBoxSort.addItem('单集动画')
        self.ComboBoxSort.addItem('季度全集')
        self.grid.addWidget(self.ComboBoxSort, 1, 0, 1, 1)
        
        self.ComboBoxTeam = ComboBox(self)
        self.ComboBoxTeam.addItem('发布组')
        team_names = [ name for name, id in teams if name != 'all']
        self.ComboBoxTeam.addItems(team_names)
        self.grid.addWidget(self.ComboBoxTeam, 1, 2, 1, 2)
        
                
    def emitArgs(self):
        args = [None, None, None]
        args[0] = self.SearchLineEdit.text()
        
        match self.ComboBoxSort.text():
            case '全部':
                args[1] = 'all'
            case '单集动画':
                args[1] = 'episode'
            case '季度全集':
                args[1] = 'season'
        
        args[2] = 'all' if self.ComboBoxTeam.text() == '发布组' else self.ComboBoxTeam.text()
        
        self.searchSignal.emit(args)
        