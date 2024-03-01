import sys
import os
file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import  QPixmap, QFontMetrics, QLinearGradient, QColor, QBrush, QPainter
from PyQt5.QtCore import Qt, pyqtSignal

from qfluentwidgets import CardWidget, RoundMenu, Action, MenuAnimationType, FluentIcon as FIF

from lib.models.subscribed_anime import SubscribedAnime

class AnimeCard(CardWidget):
    posterChanged = pyqtSignal()
    infoChanged = pyqtSignal()
    deleted = pyqtSignal()
    cleared = pyqtSignal()
    
    def __init__(self, parent, anime:SubscribedAnime):
        print(f'AnimeCard created for {anime.title}')
        super().__init__(parent)
        if not self.objectName():
            self.setObjectName(u"anime_card")
        self.anime = anime
        if anime.poster:
            self.poster = os.path.join('res', anime.title, anime.poster)
            if not os.path.exists(self.poster):
                self.poster = os.path.join('res', 'defaut.jpg')
        else:
            self.poster = os.path.join('res', 'defaut.jpg')
        self.poster = QPixmap(self.poster)
        self.posterPixmap = self.poster.copy()
        self.initUi()
        self.setClickEnabled(True) # 这个方法会调用self.update()
        
    def initUi(self):
        self.posterLabel = GradientLabel(self, self.posterPixmap)
        self.posterLabel.resize(self.width(), self.height())
        self.posterLabel.hasNew = self.anime.NewCount != 0
        
        
        # 上次看到：
        self.lastWatchedLabel = QLabel(self)
        self.lastWatchedLabel.setWordWrap(True)
        self.lastWatchedLabel.setVisible(False)
        self.lastWatchedLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lastWatchedLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.lastWatchedLabel.setStyleSheet("""
                      background-color: transparent;
                      font-size: 12px;
                      font-family: '微软雅黑';
                      color: rgb(240,240,240);
                      """)
        self.lastWatchedLabel.move(0,0)
        
        # 标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setStyleSheet("""
                                      background-color: transparent;
                                      font-size: 20px;
                                      font-family: '微软雅黑';
                                      color: rgb(240,240,240);
                                      """)
        
        # 发布组
        self.teamLabel = QLabel(self)
        self.teamLabel.setStyleSheet("""
                              background-color: transparent;
                              font-size: 15px;
                              font-family: '微软雅黑';
                              color: rgb(240,240,240);
                              """)
        
        self.adjustPos()
        
    def update(self):
        defaut_style_L = '<div style="color: black;font-size:12px;">'
        defaut_style_R = '</div>'
        
        self.titleLabel.setToolTip(defaut_style_L + self.anime.title + defaut_style_R)
        metrics = QFontMetrics(self.titleLabel.font())
        elided_text = metrics.elidedText(self.anime.title, Qt.ElideRight, self.titleLabel.width())
        self.titleLabel.setText( "<b>" + elided_text + "</b>")
        
        self.teamLabel.setToolTip(defaut_style_L + self.anime.team + defaut_style_R)
        metrics = QFontMetrics(self.teamLabel.font())
        elided_text = metrics.elidedText(self.anime.team, Qt.ElideRight, self.teamLabel.width())
        self.teamLabel.setText(elided_text)
        
        if self.anime.lastWatchedEpisode is not None:
            self.lastWatchedLabel.setToolTip(defaut_style_L + self.anime.lastWatchedEpisode.title + defaut_style_R)
            metrics = QFontMetrics(self.teamLabel.font())
            elided_text = metrics.elidedText('上次看到: '+self.anime.lastWatchedEpisode.title, Qt.ElideRight, self.teamLabel.width()*4)
            self.lastWatchedLabel.setText(elided_text)

        super().update()
        
    def crop_pixmap(self, pixmap:QPixmap):
        """裁剪pixmap, 使之与控件大小匹配"""
        original_width = pixmap.width()
        original_height = pixmap.height()
        # Calculate the aspect ratio of the original pixmap
        original_ratio =  original_height / original_width

        target_width = self.width()
        target_height = self.height()
        target_ratio = target_height / target_width

        if original_ratio < target_ratio:
            # Original pixmap is wider, crop horizontally
            cropped_width = int(original_height/target_ratio)
            x_offset = (original_width - cropped_width) // 2
            cropped_pixmap = pixmap.copy(x_offset, 0, cropped_width, original_height)
        else:
            # Original pixmap is taller, crop vertically
            cropped_height = int(original_width*target_ratio)
            y_offset = (original_height - cropped_height) // 2
            cropped_pixmap = pixmap.copy(0, y_offset, original_width, cropped_height)
            
        #print(f'Current size of the poster: width = {target_width}, height = {target_height}')

        return cropped_pixmap.scaled(target_width, target_height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    
    def adjustPos(self) -> None:
        margin = self.width()//10
        h = self.height()
        
        self.titleLabel.move(margin, 5*self.height()//8)
        self.titleLabel.resize(self.width() - 2*margin, h*2//8)
        
        self.teamLabel.move(margin, 13*self.height()//16)
        self.teamLabel.resize(self.width() - 2*margin, h*1//8)
        
        self.lastWatchedLabel.move(margin, h//20)
        self.lastWatchedLabel.setMinimumHeight(h//8)
        self.lastWatchedLabel.setMaximumHeight(h//2)
        self.lastWatchedLabel.setFixedWidth(self.width() - 2*margin)
        
    def contextMenuEvent(self, e):
        # 创建右击菜单
        menu = RoundMenu(self)
        
        submenu_edit = RoundMenu('编辑',self)
        submenu_edit.setIcon(FIF.LABEL)
        
        subaction_title = Action(FIF.TAG, '更改标题/发布组')
        subaction_title.triggered.connect(self.infoChanged)
        subaction_img = Action(FIF.PHOTO, '更改海报')
        subaction_img.triggered.connect(self.posterChanged)
        
        submenu_edit.addActions([subaction_title, subaction_img])
        menu.addMenu(submenu_edit)
        
        action_clear = Action(FIF.BROOM, '清空')
        action_clear.triggered.connect(self.cleared)
        menu.addAction(action_clear)
        
        action_delete = Action(FIF.UNPIN, '删除')
        action_delete.triggered.connect(self.deleted)
        menu.addAction(action_delete)
        
        menu.addSeparator()
        
        menu.addAction(Action(FIF.CLOSE, '取消'))
        # 显示右击菜单
        menu.exec_(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        
    def resizeEvent(self, a0) -> None:
        self.adjustPos()
        self.update()
        self.posterPixmap = self.crop_pixmap(self.poster)
        try:
            self.posterLabel.resize(self.width(), self.height())
            self.posterLabel.setBackgroundImg(self.posterPixmap)
        except AttributeError:
            pass
        return super().resizeEvent(a0)
    
    def enterEvent(self, event):
        self.posterLabel.hover = True
        self.posterLabel.update()
        
        self.lastWatchedLabel.setVisible(True)

    def leaveEvent(self, event):
        self.posterLabel.hover = False
        self.posterLabel.update()
        
        self.lastWatchedLabel.setVisible(False)

class GradientLabel(QLabel):
    hover:bool = False
    hasNew:bool = False
    
    def __init__(self, parent, pixmap: QPixmap):
        super().__init__(parent)
        self.pixmap = pixmap
        self.setMouseTracking(True)
    
    def setBackgroundImg(self, pixmap: QPixmap):
        if isinstance(pixmap, QPixmap):
            self.pixmap = pixmap
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

        # 创建渐变效果
        gradient_start_pos = self.height()//3
        gradient = QLinearGradient(0, gradient_start_pos, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        if self.hasNew:
            gradient.setColorAt(1, QColor(120, 70, 0, 200))
        else:
            gradient.setColorAt(1, QColor(0, 0, 0, 200)) # 最暗处的alpha值
        
        if not self.hover:
            # 应用渐变
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, gradient_start_pos, self.width(), self.height() - gradient_start_pos)
        else:
            # 如果悬停，则完全变暗
            if self.hasNew:
                painter.setBrush(QColor(120, 70, 0, 150))
            else:
                painter.setBrush(QColor(0, 0, 0, 150))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())

        painter.end()
        
