import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(root_path)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QHeaderView, QTableWidgetItem

from qfluentwidgets import TableWidget, RoundMenu, Action, MenuAnimationType, FluentIcon as FIF
import pyperclip

from lib.models.anime import Anime


class AnimeEpisodesTable(TableWidget):
    episodes:list[Anime] = []
    selected_indexes:set = set()
    unwatchedOnly: bool = False
    marked = pyqtSignal(int)
    unmarked = pyqtSignal(int)
    
    def __init__(self, parent) -> None:
        super().__init__(parent)

        header_labels = ['Title', 'Publishing Date']
        self.setColumnCount(len(header_labels))
        self.setMinimumHeight(15)
        self.setHorizontalHeaderLabels(header_labels)
        
        self.setColumnWidth(0, self.width()*7//10)
        self.setRowCount(50)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        
        
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.setWordWrap(True)
        
        self.cellClicked.connect(self.__onCellClicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__show_context_menu)
        
        self.itemSelectionChanged.connect(self.__onSelectionChanged)
        
        self.show()

    def setData(self, data:list[Anime]):
        self.episodes = data
        self.update()
        
    def setUnwatchedOnly(self, isUnwatchedOnly = True):
        self.unwatchedOnly = isUnwatchedOnly
        self.update()
        

    def update(self):
        self.clear()
        if self.unwatchedOnly:
            self.setRowCount(
                len([episode for episode in self.episodes if not episode.watched])
            )
        else:
            self.setRowCount(len(self.episodes))
        row = 0
        for index, episode in enumerate(self.episodes):
            if not self.unwatchedOnly or not episode.watched:
                title_cell = QTableWidgetItem(episode.title)
                title_cell.setData(Qt.UserRole,index)
                title_cell.setFlags(title_cell.flags()& ~Qt.ItemIsEditable)
                title_cell.setToolTip(episode.title + '\n--单击以复制磁力链--')
                date_cell = QTableWidgetItem(str(episode.pubDate))
                date_cell.setFlags(date_cell.flags()& ~Qt.ItemIsEditable)
                date_cell.setToolTip('发布于\n'+str(episode.pubDate))
                self.setItem(row, 0, title_cell)
                self.setItem(row, 1, date_cell)
                row += 1
        super().update()
        
    def clear(self):
        super().clear()
        header_labels = ['Title', 'Publishing Date']
        self.setHorizontalHeaderLabels(header_labels)

        
    
    def __onCellClicked(self, row, col):
        item = self.item(row, col)
        index = item.data(Qt.UserRole)
        if col == 0:
            print(f'Item clicked: index = {index}')
            pyperclip.copy(self.episodes[index].magnet)
            
    def __copyMultipleMagnets(self):
        print(f'Magnet copied for:')
        magnet = []
        for index in self.selected_indexes:
            magnet.append(self.episodes[index].magnet)
            print(self.episodes[index].title)
        copied = '\n'.join(magnet)
        pyperclip.copy(copied)
        
    def __onSelectionChanged(self):
        items = self.selectedIndexes()
        self.selected_indexes.clear()
        for item in items:
            row = item.row()
            cell = self.item(row, 0)
            self.selected_indexes.add(cell.data(Qt.UserRole))
        print(f'Selected indexes: {self.selected_indexes}')
        
    def __show_context_menu(self, pos):
        # 获取全局坐标
        global_pos = self.mapToGlobal(pos)
        
        # 获取右击的行数
        row = self.rowAt(pos.y())
        
        item = self.item(row, 0)
        index = item.data(Qt.UserRole)
        
        # 创建右击菜单
        menu = RoundMenu(self)
        
        if self.episodes[index].watched:
            action_unmark = Action(FIF.CANCEL, "标记为未看")
            action_unmark.triggered.connect(lambda: self.unmarked.emit(index))
            action_unmark.triggered.connect(self.update)
            menu.addAction(action_unmark)
        else:
            action_mark = Action(FIF.COMPLETED, '标记为看过')
            action_mark.triggered.connect(lambda: self.marked.emit(index))
            action_mark.triggered.connect(self.update)
            menu.addAction(action_mark)
        
        if len(self.selected_indexes) <= 1:
            action_copy = Action(FIF.COPY, '复制磁力链')
            action_copy.triggered.connect(lambda: pyperclip.copy(self.episodes[row].magnet))
            menu.addAction(action_copy)
        
        menu.addSeparator()
        
        if len(self.selected_indexes) > 1:
            action_copy_selected = Action(FIF.COPY, '复制选中的磁力链')
            action_copy_selected.triggered.connect(self.__copyMultipleMagnets)
            menu.addAction(action_copy_selected)
    
        menu.addAction(Action(FIF.CLOSE, '取消'))
        # 显示右击菜单
        menu.exec_(global_pos, aniType=MenuAnimationType.DROP_DOWN)
            
    def resizeEvent(self, e):
        super().resizeEvent(e)
        return self.setColumnWidth(0, self.width()*7//10)