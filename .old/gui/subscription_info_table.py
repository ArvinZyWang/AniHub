import pyperclip
from qfluentwidgets import TableWidget, RoundMenu, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal


class UnwatchedAnime(TableWidget):
    
    marked = pyqtSignal(int)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.anime_new_list = []
        
        header_labels = ['Title', 'Pub Date']
        self.setColumnCount(len(header_labels))
        self.setRowCount(5)
        self.setMinimumHeight(10)
        self.setHorizontalHeaderLabels(header_labels)
        
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        
        self.resize(590,200)
        self.setColumnWidth(0,450)
        
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.setWordWrap(True)
        
        self.cellClicked.connect(self.on_cell_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.show()

    
    def update(self, anime_new_list:list[dict]):
        self.anime_new_list = anime_new_list
        self.setRowCount(len(anime_new_list))
        
        for row, item in enumerate(anime_new_list):
            dict = item
            item_0 = QTableWidgetItem(dict['title'])
            item_0.setFlags(item_0.flags()& ~Qt.ItemIsEditable)
            item_0.setToolTip(dict['title'] + '\n单击以复制磁力链')
            item_1 = QTableWidgetItem(str(dict['pubDate']))
            item_1.setFlags(item_1.flags()& ~Qt.ItemIsEditable)
            self.setItem(row, 0, item_0)
            self.setItem(row, 1, item_1)
            
    
    def on_cell_clicked(self, row, col):
        if self.anime_new_list and col == 0 and row < len(self.anime_new_list):
            pyperclip.copy(self.anime_new_list[row]['magnet'])
            
    
    def show_context_menu(self, pos):
        # 获取全局坐标
        global_pos = self.mapToGlobal(pos)
        
        # 获取右击的行数
        row = self.rowAt(pos.y())
        
        if 0 <= row < len(self.anime_new_list):
            # 创建右击菜单
            menu = RoundMenu(self)
            
            # 添加动作，可以根据需要添加更多
            action_mark = Action(FIF.COMPLETED, '标记为看过')
            action_mark.triggered.connect(lambda: self.marked.emit(row))
            menu.addAction(action_mark)
            
            action_copy = Action(FIF.COPY, '复制磁力链')
            action_copy.triggered.connect(lambda: pyperclip.copy(self.anime_new_list[row]['magnet']))
            menu.addAction(action_copy)
            
            menu.addSeparator()
        
            menu.addAction(Action(FIF.CLOSE, '取消'))
            # 显示右击菜单
            menu.exec_(global_pos, aniType=MenuAnimationType.DROP_DOWN)
        
        
if __name__ =='__main__':
    from PyQt5.QtWidgets import QApplication, QWidget
    import sys, os
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.append(project_root)
    import utils.update_manager as um
    
    class test(QWidget):
        
        def __init__(self, parent = None) -> None:
            super().__init__(parent)
            self.initUI()
            self.resize(800, 700)
            
        def initUI(self):
            ###
            t = UnwatchedAnime(self)
            t.update(um.load_subscription()[0]['New'])
            ###
            self.show()
            
    
    app = QApplication(sys.argv)
    test_window = test(None)
    sys.exit(app.exec_())
