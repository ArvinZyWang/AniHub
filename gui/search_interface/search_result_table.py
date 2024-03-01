import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(root_path)

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, 
                             QHeaderView, QTableWidgetItem, QAbstractItemView)

from qfluentwidgets import (TableWidget, PushButton, Action,
                            RoundMenu, MenuAnimationType,
                            FluentIcon as FIF)
import pyperclip

from lib.models.anime import Anime


class SearchResultTable(QWidget):
    data:list[Anime] = []
    
    __current_page:int = 0
    __total_page_count: int = 0
    
    selected_indexes:set = set()
    
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.resize(650, 500)
        
    def initUi(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.Table = TableWidget(self)
        self.grid.addWidget(self.Table, 0, 0, 11, 9)
        headerLables = ['Title', 'Publishing Date']
        self.Table.setColumnCount(len(headerLables))
        self.Table.setRowCount(10)
        self.Table.setHorizontalHeaderLabels(headerLables)
        
        # 设定表头宽度，隐藏垂直表头
        self.Table.setColumnWidth(0, self.width()*7//10)
        self.Table.verticalHeader().setVisible(False)
        self.Table.horizontalHeader().setStretchLastSection(True)
        # 设置行高
        for row in range(10):
            self.Table.setRowHeight(row, self.height()//10)
        self.Table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.Table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            
        self.Table.setBorderRadius(8)
        self.Table.setBorderVisible(True)
        self.Table.setWordWrap(True)
        self.Table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        self.Table.cellClicked.connect(self.__onCellClicked)
        self.Table.itemSelectionChanged.connect(self.__onSelectionChanged)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        
        self.ButtonPrev = PushButton(self)
        self.ButtonPrev.setText('上一页')
        self.ButtonPrev.clicked.connect(self.__prevPage)
        self.grid.addWidget(self.ButtonPrev, 11, 3, 1, 1)
        
        self.ButtonNext = PushButton(self)
        self.ButtonNext.setText('下一页')
        self.ButtonNext.clicked.connect(self.__nextPage)
        self.grid.addWidget(self.ButtonNext, 11, 5, 1, 1)
        
        self.LableCount = QLabel(self)
        self.LableCount.setText(' ')
        self.LableCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.LableCount, 11, 4, 1, 1)
        
        
        self.show()
        self.update()
        
    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        return self.Table.setColumnWidth(0, self.width()*7//10)
        
        
    def update(self):
        max_index = (self.__current_page+1)*10
        min_index = self.__current_page*10
        
        selected_indexes = list(range(min_index, max_index))
        for row, index in enumerate(selected_indexes):
            title_cell = QTableWidgetItem(self.data[index].title) if index < len(self.data) else QTableWidgetItem(None)
            date_cell = QTableWidgetItem(str(self.data[index].pubDate)) if index < len(self.data) else QTableWidgetItem(None)
            
            title_cell.setFlags(title_cell.flags()& ~Qt.ItemIsEditable) # 使Cell不可双击修改
            date_cell.setFlags(title_cell.flags()& ~Qt.ItemIsEditable)
            
            # 设置ToolTip（鼠标悬停）
            if index < len(self.data):
                title_cell.setToolTip(self.data[index].title + '\n--单击以复制磁力链--')
                date_cell.setToolTip('发布于\n' + str(self.data[index].pubDate))
                
            self.Table.setRowHidden(row, index >= len(self.data))
            
            self.Table.setItem(row, 0, title_cell)
            self.Table.setItem(row, 1, date_cell)
        self.LableCount.setText(f'{self.__current_page + 1 }/{self.__total_page_count}')
        
        # 设置上一页/下一页按钮的启用/禁用
        self.ButtonPrev.setDisabled(self.__current_page <= 0)
        self.ButtonNext.setDisabled(self.__current_page >= self.__total_page_count - 1)
        
        super().update()
        
    def __prevPage(self):
        if  0 < self.__current_page < self.__total_page_count:
            self.__current_page -= 1
            self.Table.clearSelection()
            self.selected_indexes.clear()
            self.update()
    
    def __nextPage(self):
        if  0 <= self.__current_page < self.__total_page_count - 1:
            self.__current_page += 1
            self.Table.clearSelection()
            self.selected_indexes.clear()
            self.update()
            
    def __onCellClicked(self, row, col):
        print(f'Cell clicked at row={row}, col={col}')
        if col == 0:
            selected = self.__current_page*10 + row
            if selected < len(self.data):
                magnet = self.data[selected].magnet
                pyperclip.copy(magnet)
                print(f'Magnet copied for {self.data[selected].title}')

    def copyMultipleMagnet(self):
        print(f'Magnet copied for:')
        magnet = []
        for index in self.selected_indexes:
            magnet.append(self.data[index].magnet)
            print(self.data[index].title)
        copied = '\n'.join(magnet)
        pyperclip.copy(copied)
    
    def setData(self, data: list[Anime]):
        self.data = data
        self.__current_page = 0
        self.__total_page_count = ( len(self.data) + 10 - 1 ) // 10
        
    def __onSelectionChanged(self):
        items = self.Table.selectedIndexes()
        self.selected_indexes.clear()
        for item in items:
            row = item.row()
            self.selected_indexes.add(row + self.__current_page*10)
        print(f'Selected indexes: {self.selected_indexes}')
            
    def show_context_menu(self, pos):
        # 获取全局坐标
        global_pos = self.mapToGlobal(pos)
        
        # 获取右击的行数
        row = self.Table.rowAt(pos.y())
        # 处理row = -1 的特殊返回值
        row = ( 9 if self.__current_page + 1 < self.__total_page_count else (len(self.data) - 1) % 10 ) if row == -1 else row - 1
        
        print(f"Right clicked at row {row}")
        
        if 0 <= row <= 9:
            # 创建右击菜单
            menu = RoundMenu(self)
            
            action_copy = Action(FIF.COPY, '复制磁力链')
            action_copy.triggered.connect(lambda row: pyperclip.copy(self.data[row + self.__current_page*10].magnet))
            action_copy.triggered.connect(lambda row: print( f'Magnet copied for: {self.data[row + self.__current_page*10].title}'))
            menu.addAction(action_copy)
            
            menu.addSeparator()
            
            if len(self.selected_indexes) > 1:
                action_copy_selected = Action(FIF.COPY, '复制选中的磁力链')
                action_copy_selected.triggered.connect(self.copyMultipleMagnet)
                menu.addAction(action_copy_selected)
        
            menu.addAction(Action(FIF.CLOSE, '取消'))
            # 显示右击菜单
            menu.exec_(global_pos, aniType=MenuAnimationType.DROP_DOWN)
            
            
    
    


