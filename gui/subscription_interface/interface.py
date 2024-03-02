import sys
import os
import shutil

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QMessageBox, QFileDialog

from qfluentwidgets import PrimaryPushButton, PushButton, SwitchButton, VerticalSeparator, SubtitleLabel, StateToolTip, FluentIcon as FIF

from anime_gallery_scroll import AnimeGalleryScroll
from anime_episodes_table import AnimeEpisodesTable
from add_anime_messagebox import AddAnimeMessageBox
from change_info_messagebox import ChangeInfoMessagebox

from lib.subscription import Subscription, SubscribedAnime
from lib.crawler.update_multithread import UpdateMultiThread
from lib.crawler.img_downloader_multithread import PosterDownloaderMultithread

class SubscriptionInterface(QWidget):
    unwatchedOnly:bool = False
    currentIndex:int = None
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.subscription = Subscription()
        self.initUi()
        self.setting()
        self.show()
        
    def initUi(self):
        total_layout = QHBoxLayout()
        self.setLayout(total_layout)
        
        ## 左侧
        left_side_layout = QVBoxLayout()
        left_side_layout.setContentsMargins(30,30,30,30)
        total_layout.addLayout(left_side_layout)
        # 占位符
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        left_side_layout.addSpacerItem(spacer)
        # 第一行
        button_line_layout = QHBoxLayout()
        self.update_btn = PrimaryPushButton(FIF.SYNC, "检查更新", self)
        self.add_btn = PushButton(FIF.ADD, "添加订阅", self)
        spacer_btn_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        spacer_btn_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        button_line_layout.addWidget(self.update_btn)
        button_line_layout.addSpacerItem(spacer_btn_1)
        button_line_layout.addWidget(self.add_btn)
        button_line_layout.addSpacerItem(spacer_btn_2)
        left_side_layout.addLayout(button_line_layout)
        # 占位符
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        left_side_layout.addSpacerItem(spacer)
        # 第二行
        above_table_layout = QHBoxLayout()
        self.titleLabel = SubtitleLabel(self)
        self.titleLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        above_table_layout.addWidget(self.titleLabel)
        above_table_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        inner_layout = QHBoxLayout()
        above_table_layout.addLayout(inner_layout)
        self.unwatchedOnlySwitch = SwitchButton(self)
        label = QLabel("仅显示未观看的剧集: ", self)
        label.setStyleSheet("""font-family: '微软雅黑'""")
        label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        inner_layout.addWidget(label)
        inner_layout.addWidget(self.unwatchedOnlySwitch)
        left_side_layout.addLayout(above_table_layout)
        # 表格
        self.table = AnimeEpisodesTable(self)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_side_layout.addWidget(self.table)
        
        
        ## 两侧分割线
        separator = VerticalSeparator(self)
        separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        total_layout.addWidget(separator)
        
        ## 右侧
        self.gallery = AnimeGalleryScroll(self, self.subscription)
        self.gallery.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        total_layout.addWidget(self.gallery)
        
        total_layout.setStretch(0, 3)
        total_layout.setStretch(2, 2)
        
    def setting(self):
        self.update_btn.clicked.connect(self.startUpdate)
        self.add_btn.clicked.connect(self.addAnimeDialog)
        
        self.unwatchedOnlySwitch.checkedChanged.connect(self.onSwitchClicked)
        self.unwatchedOnlySwitch.setChecked(True)
        
        if len(self.subscription.data) != 0:
            self.onItemClicked(0)
        # currentAnime = self.subscription.data[self.currentIndex]
        self.table.marked.connect(lambda i: self.onMarkedAsWatched(i))
        self.table.unmarked.connect(lambda i: self.onMarkedAsUnwatched(i))
        
        self.gallery.clicked.connect(lambda index: self.onItemClicked(index))
        self.gallery.infoChanged.connect(lambda index: self.onInfoChanged(index))
        self.gallery.posterChanged.connect(lambda index: self.onPosterChanged(index))
        self.gallery.deleted.connect(lambda index: self.onItemDeleted(index))
        self.gallery.cleared.connect(lambda index: self.onEpisodesClear(index))
    
    def onSwitchClicked(self):
        self.unwatchedOnly = self.unwatchedOnlySwitch.isChecked()
        self.table.setUnwatchedOnly(self.unwatchedOnly)
        
    ################
    ###Tabel Slot###    
    def onMarkedAsWatched(self, index):
        needUpdate = False
        currentAnime = self.subscription.data[self.currentIndex]
        currentAnime.markAsWatched(index)
        if currentAnime.NewCount <= 0:
            needUpdate = True
        if needUpdate:
            self.gallery.update()
        
    def onMarkedAsUnwatched(self, index):
        needUpdate = False
        currentAnime = self.subscription.data[self.currentIndex]
        if currentAnime.NewCount <= 0:
            needUpdate = True
        currentAnime.markAsUnwatched(index)
        if needUpdate:
            self.gallery.update()
    ###Tabel Slot###
    ################
    
    ###################  
    ### Galley Slot ###
    def onItemClicked(self, index):
        self.currentIndex = index
        clickedAnime:SubscribedAnime = self.subscription.data[index]
        print(f'Anime {clickedAnime.title} is clicked.')
        self.table.setData(clickedAnime.episodes)
        self.titleLabel.setText(clickedAnime.title)
        
    def onInfoChanged(self, index):
        selected_anime:SubscribedAnime = self.subscription.data[index]
        print(f'Edit info of {selected_anime.title}.')
        dialog = ChangeInfoMessagebox(self, selected_anime)
        args = None
        if dialog.exec_():
            print(f"Subscription {selected_anime.title}@{selected_anime.team} changed to: {dialog.args[0]}@{dialog.args[1]}")
            args = dialog.args
        if args:
            new_title = args[0]
            new_team = args[1]
            selected_anime.edit(new_title, new_team)
            # 若不使用QTimer, 直接进行界面更新，将会违反Qt线程安全规定，导致程序退出
            QTimer.singleShot(0, self.update)

    
    def onPosterChanged(self, index):
        selected_anime:SubscribedAnime = self.subscription.data[index]
        print(f'Change poster for {selected_anime.title}.')
        imgPath = os.path.join(root_path, "res", selected_anime.title)
        if not os.path.exists(imgPath) or len(os.listdir(imgPath)) == 0:
            print(f'No poster avaliable for {selected_anime.title}')
        else:
            filter = "Image Files (*.jpeg *.jpg *.png *.bmp *.gif *.webp)"
            target_img, _ = QFileDialog.getOpenFileName(self, '选择海报', imgPath, filter)
            target_img_name = os.path.basename(target_img)
            if target_img:
                target_img_destination = os.path.join(imgPath, target_img_name)
                if not os.path.exists(target_img_destination):
                # 如果图片不在目标路径中，复制图片到目标路径
                    shutil.copy(target_img, target_img_destination)
                selected_anime.poster = target_img_name
                selected_anime.save()
                # 若不使用QTimer, 直接进行界面更新，将会违反Qt线程安全规定，导致程序退出
                QTimer.singleShot(0, self.update)

        
    def onItemDeleted(self, index):
        selected_anime:SubscribedAnime = self.subscription.data[index]
        print(f'Delete {selected_anime.title} from subscription.')
        reply = QMessageBox.question(
            None, '取消订阅', f'是否删除 <b>{selected_anime.title}</b> @{selected_anime.team}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.currentIndex == index:
                if len(self.subscription.data) > 0:
                    self.onItemClicked(0)
                else:
                    self.table.clear()
            self.subscription.remove(index)
            self.update()
            
    def onEpisodesClear(self, index):
        currentAnime:SubscribedAnime = self.subscription.data[index]
        print(f'Clear Episodes for {currentAnime.title}')
        currentAnime.episodes.clear()
        currentAnime.save()
        self.onItemClicked(index)
    ### Galley Slot ###
    ###################
    def startUpdate(self):
        updateThread = UpdateMultiThread(self.subscription)
        print('Start to update.')
        self.stateTooltip = StateToolTip('Update', '正在拉取更新，建议挂上代理哦~', self.gallery)
        self.stateTooltip.show()
        updateThread.start()
        loop = QEventLoop()
        updateThread.finished.connect(self.onUpdateFinished)
        updateThread.finished.connect(loop.quit)
        loop.exec_()
        
    def onUpdateFinished(self):
        print('Update completed.')
        self.onItemClicked(self.currentIndex)
        posterDownloadThread = PosterDownloaderMultithread(self.subscription)
        if self.stateTooltip:
            self.stateTooltip.setContent("正在更新海报~")
        posterDownloadThread.start()
        loop = QEventLoop()
        posterDownloadThread.finished.connect(self.onPosterLoaded)
        loop.exec_()
        
    def onPosterLoaded(self):
        print('Poster Downloaded.')
        self.stateTooltip.setContent("更新完成ヾ(*´▽'*)ﾉ")
        self.stateTooltip.setState(True)
        self.stateTooltip = None
        self.update()
        
    def addAnimeDialog(self):
        dialog = AddAnimeMessageBox(self)
        if dialog.exec():
            print(f"Subscription added: {dialog.args[0]}@{dialog.args[1]}")
            self.subscription.add(*dialog.args)
            self.gallery.update()
            self.startUpdate()
            if dialog.args == None:
                return
        
    def update(self):
        self.gallery.update()
        super().update()
        