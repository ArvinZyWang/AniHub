from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QMessageBox
from PyQt5.QtGui import  QPixmap, QFont, QColor
from qfluentwidgets import RoundMenu, Action, MenuAnimationType, SmoothScrollArea
from qfluentwidgets import FluentIcon as FIF

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
import utils.update_manager as um


class AnimeContainer(QWidget):
    """
    展示动画信息的盒子，信息有：海报、标题、发布组。

    单击时发送信号clicked, 信号携带动画的编号anime_index
    右击菜单有编辑、删除
    删除功能触发后发送信号item_deleted
    """
    
    clicked = pyqtSignal(int)
    item_deleted = pyqtSignal()
    item_title_change = pyqtSignal(int)
    item_img_change = pyqtSignal(int)
    
    def __init__(self, parent, anime_info:dict, anime_index:int) -> None:
        
        super().__init__(parent)
        self.setFixedSize(140, 205)
        
        self.index = anime_index
        self.title = anime_info['title']
        self.team = anime_info['team']
        
        try:
            img = anime_info['img']
            imgPath = os.path.join(project_root, "res", self.title, img)
        except:
            img = 'defaut_img.jpg'
            imgPath = os.path.join(project_root, "res", img)
        
        self.setToolTip(self.title)
        
        # 背景颜色
        self.background = QFrame(self)
        backgroundColor = QColor(252,252,252)
        self.background.setStyleSheet(f"background-color: {backgroundColor.name()};"
                                        "border-radius: 20px;")
        self.background.setGeometry(0,0,140,205)
        
        # 海报图片
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(20, 20, 100, 141)
        pixmap = QPixmap(imgPath)
        pixmap = self.crop_pixmap(pixmap, 100, 141)
        self.imageLabel.setPixmap(pixmap)
        
        # 右上角的红点
        self.new_count = len(anime_info['New'])
        self.update_label = QLabel(self)
        self.update_label.setGeometry(110, 15, 17, 17)
        self.update_label.setStyleSheet("""
            background-color: rgb(201, 071, 055);
            border-radius: 8px; 
            color: rgb(217, 237, 235);
            font-weight: bold;
            text-align: center;
            font: 10pt "Nirmala UI";
        """)
        self.update_label.setAlignment(Qt.AlignCenter)
        if self.new_count > 0:
            self.update_label.setText(str(self.new_count))
            self.update_label.show()
        else:
            self.update_label.hide()        
        
        # 标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(0, 165, 140, 15)
        font = QFont()
        font.setPointSize(11)
        font.setFamilies([u"\u9ed1\u4f53"])
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setText(self.title)
        self.titleLabel.setWordWrap(True)

        # 发布组
        self.teamLabel = QLabel(self)
        self.teamLabel.setGeometry(0, 182, 140, 15)
        font1 = QFont()
        font1.setPointSize(8)
        font1.setFamilies([u"\u534e\u6587\u7ec6\u9ed1"])
        self.teamLabel.setFont(font1)
        self.teamLabel.setAlignment(Qt.AlignHCenter)
        self.teamLabel.setText(self.team)
    
    
    @staticmethod
    def crop_pixmap(pixmap: QPixmap, width, height) -> QPixmap:
        """Crop the pixmap to the specified width and height."""
        original_width = pixmap.width()
        original_height = pixmap.height()

        # Calculate the aspect ratio of the target size
        target_ratio = width / height

        # Calculate the aspect ratio of the original pixmap
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            # Original pixmap is wider, crop horizontally
            new_width = int(original_height * target_ratio)
            x_offset = (original_width - new_width) // 2
            cropped_pixmap = pixmap.copy(x_offset, 0, new_width, original_height)
        else:
            # Original pixmap is taller, crop vertically
            new_height = int(original_width / target_ratio)
            y_offset = (original_height - new_height) // 2
            cropped_pixmap = pixmap.copy(0, y_offset, original_width, new_height)

        # Scale the cropped pixmap to the target size
        return cropped_pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

    def mousePressEvent(self, event):
        # 按下左键时发送信号clicked
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)

    def contextMenuEvent(self, e):
        """右击菜单"""
        menu = RoundMenu(parent=self)
        
        submenu_edit = RoundMenu('编辑',self)
        submenu_edit.setIcon(FIF.LABEL)
        subaction_title = Action(FIF.TAG, '更改标题/发布组')
        subaction_title.triggered.connect(lambda: self.item_title_change.emit(self.index))
        subaction_img = Action(FIF.PHOTO, '更改海报')
        subaction_img.triggered.connect(lambda: self.item_img_change.emit(self.index))
        submenu_edit.addActions([subaction_title, subaction_img])
        menu.addMenu(submenu_edit)
        
        action_delete = Action(FIF.UNPIN, '删除')
        action_delete.triggered.connect(self.menuDelete)
        menu.addAction(action_delete)
        
        menu.addSeparator()
        
        menu.addAction(Action(FIF.CLOSE, '取消'))
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

        
    def menuDelete(self):
        reply = QMessageBox.question(
            None, '取消订阅', f'是否删除 <b>{self.title}</b> @{self.team}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            subscription_data = um.load_subscription()
            current_anime = subscription_data[self.index]
            if current_anime['title'] == self.title:
                subscription_data.remove(current_anime)
            um.update_subscription(subscription_data)
            self.item_deleted.emit()
        

class ScrollArea(SmoothScrollArea):
    
    def __init__(self, parent, child:QWidget):
        super().__init__(parent)
        
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFrameStyle(QFrame.NoFrame)
        
        self.horizontalScrollBar().setValue(child.height())
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)
        self.setStyleSheet("""
            SubscribedAnimePage {
                background-color: rgb(232,232,232);  /* 设置背景颜色为灰色 */
                border-radius: 10px;        /* 添加圆角矩形效果，根据需要调整圆角半径 */
            }
        """)

        self.setWidget(child)
        self.resize(590, 300)
        
        
    
class SubscribedAnimePage(QWidget):
    itemClicked = pyqtSignal(int)
    itemDeleted = pyqtSignal()
    itemEdit =pyqtSignal(list)
    
    def __init__(self, parent:QWidget) -> None:
        super().__init__(parent)
        self.resize(590, 450)
        self.update_from_data()
        
        
    def update_from_data(self):
        for child in self.findChildren(QWidget):
            child.deleteLater()
            
        self.subscription_data = um.load_subscription()
        items_per_row = 4
        verticalSpace = 10
        horizontalSpace = 5
        
        row_counts = (len(self.subscription_data) + items_per_row - 1)// items_per_row
        row = 0
        col = 0
        
        
        for anime_index, anime_info in enumerate(self.subscription_data):
            row = anime_index // items_per_row
            col = anime_index % items_per_row
            
            # 链接信号
            anime_container = AnimeContainer(self, anime_info, anime_index)
            anime_container.clicked.connect(self.item_clicked)
            anime_container.item_deleted.connect(self.item_deleted)
            anime_container.item_img_change.connect(lambda index: self.itemEdit.emit(['img', index]))
            anime_container.item_title_change.connect(lambda index: self.itemEdit.emit(['title', index]))
            
            horizontal_pos = [i*(anime_container.width()+ horizontalSpace) + 5 for i in range(items_per_row)] # .width后加的数为水平间隙
            vertical_pos = [i*(anime_container.height()+ verticalSpace) + 5 for i in range(row_counts)] # .height后加的数为垂直间隙
            
            anime_container.move(horizontal_pos[col], vertical_pos[row])
            anime_container.show()
            
            if vertical_pos[row] + anime_container.height() > self.height():
                self.resize(590, vertical_pos[row] + anime_container.height())
        
        self.show()
    
    
    def item_clicked(self, anime_index):
        self.itemClicked.emit(anime_index)
    
    def item_deleted(self):
        self.itemDeleted.emit()
        
        
if __name__ == '__main__':
    test_info ={
        'title': '葬送的芙莉莲',
        'team': 'LoliHouse',
    }
    from PyQt5.QtWidgets import QApplication
    import sys
    
    class test(QWidget):
        
        def __init__(self, parent = None) -> None:
            super().__init__(parent)
            self.resize(500, 500)
            self.initUI()
            
        def initUI(self):
            ###
            t = ScrollArea(self,SubscribedAnimePage(self))
            self.show()
        
    app = QApplication(sys.argv)    
    test_window = test()
    sys.exit(app.exec_())