import pyperclip
from qfluentwidgets import TableWidget, PushButton
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QHeaderView
from PyQt5.QtCore import Qt


class SearchResult(TableWidget):
    
    def __init__(self, parent, pos:list[int]):
        super().__init__(parent)
        self.page = 0
        self.result = []
        self.selected_items = []
        
        header_labels = ['Title', 'Pub Date']
        self.setColumnCount(len(header_labels))
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(header_labels)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        
        self.setGeometry(pos[0],pos[1],650,475)
        self.setColumnWidth(0,500)
        
        
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.setWordWrap(True)
        
        self.btn_prev = PushButton(self)
        self.btn_prev.setText('上一页')
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_prev.move(200, 430)
        self.setCellWidget(10,1, self.btn_prev)
        
        self.btn_next = PushButton(self)
        self.btn_next.setText('下一页')
        self.btn_next.clicked.connect(self.next_page)
        self.btn_next.move(400, 430)
        self.setCellWidget(10,2, self.btn_next)
        
        self.count = QLabel(self)
        self.count.setText(f' ')
        self.count.move(315, 440)
        
        font = self.count.font()
        font.setPointSize(9)  # 设置字号
        font.setFamily('Segoe UI')

        self.count.setFont(font)    # 将字体应用到 QLabel
        self.setCellWidget(10,1, self.count)
        self.count.resize(53,15)
        
        self.cellClicked.connect(self.on_cell_clicked)
        
        self.show()

    
    def update(self):
        assert not self.result is []
        
        max_page = min((self.page+1)*10, len(self.result))
        self.selected_items = range(self.page*10, max_page)
        
        for row, item in enumerate(self.selected_items):
            dict = self.result[item]
            item_0 = QTableWidgetItem(dict['title'])
            item_0.setFlags(item_0.flags()& ~Qt.ItemIsEditable)
            item_0.setToolTip(dict['title'] + '\n单击以复制磁力链')
            item_1 = QTableWidgetItem(str(dict['pubDate']))
            item_1.setFlags(item_1.flags()& ~Qt.ItemIsEditable)
            self.setItem(row, 0, item_0)
            self.setItem(row, 1, item_1)

            
        total_pages = (len(self.result) + 10 -1 ) // 10
        count = f'{self.page +1 } / {total_pages}'
        self.count.setText(count)
            
    
    def on_cell_clicked(self, row, col):
        if col == 0 and row < len(self.selected_items):
            pyperclip.copy(self.result[self.selected_items[row]]['magnet'])
    
    def next_page(self):
        if self.page < len(self.result) - 1:
            self.page += 1
            self.update()
        else:
            return
        
    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update()
        else:
            return
        
if __name__ =='__main__':
    from PyQt5.QtWidgets import QApplication
    import sys 
    app = QApplication(sys.argv)    
    test_window = SearchResult(None,[0,0])
    sys.exit(app.exec_())
