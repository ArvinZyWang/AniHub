from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QFileDialog

from add_anime_messagebox import AddAnimeMessageBox
from anime_container import SubscribedAnimePage, ScrollArea
from subscription_info_table import UnwatchedAnime

from qfluentwidgets import RoundMenu, Action,MenuAnimationType, Flyout, InfoBarIcon
from qfluentwidgets import FluentIcon as FIF


import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
from utils import update_manager as um
from utils import scraper


class SubscriptionInterface(QWidget):
    """
    右击更新
    表格右击：标记为看过， 复制磁力链， 取消
    """
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.resize(750,700)
        self.subscription_data = um.load_subscription()
        
        self.subscribed_anime_page = SubscribedAnimePage(self)
        self.subscribed_anime_page.itemClicked.connect(self.update_table)
        self.subscribed_anime_page.itemDeleted.connect(self.update_data)
        self.subscribed_anime_page.itemEdit.connect(self.itemEdit)
        
        self.scroll_area = ScrollArea(self, self.subscribed_anime_page)
        self.scroll_area.move(110,50)
        
        self.infotable = UnwatchedAnime(self)
        self.infotable.marked.connect(self.mark_as_watched)
        self.infotable.move(110,420)
        
        
    def update_data(self):
        """更新订阅页的内容"""
        self.subscription_data = um.load_subscription()
        self.subscribed_anime_page.update_from_data()

    def itemEdit(self, args):
        """展示页菜单 - 编辑"""
        sort, index = args
        
        anime_info = self.subscription_data[index]
        title = anime_info['title']
        team = anime_info['team']
        imgpath = os.path.join(project_root, 'res', title)
        
        if sort == 'img':
            # 更改选中对象的海报
            
            # 如果不存在可用的海报，则提示：
            if not os.path.exists(imgpath) or len(os.listdir(imgpath)) == 0:
                Flyout.create(
                    icon=InfoBarIcon.ERROR,
                    title='图片尚未载入完毕',
                    content="请等待图片载入！",
                    target=self.subscribed_anime_page,
                    parent=self,
                    isClosable=True
                    )
            else:
                target_img, _ = QFileDialog.getOpenFileName(self, '选择海报', imgpath,
                                                   'All Files (*)')
                if target_img:
                    self.subscription_data[index]['img'] = target_img.split('/')[-1]
                    um.update_subscription(self.subscription_data)
                    self.update_data()
                    
        if sort == 'title':
            # 更改选中对象的标题或发布组
            dialog = AddAnimeMessageBox(self.parent())
            dialog.titleLabel.setText('更改订阅信息')
            dialog.LineEdit.setText(title)
            dialog.teamComboBox.setText(team)
            if dialog.exec():
                target_title, target_team = dialog.args
                if not (title == target_title and team == target_team):
                    self.subscription_data[index]['title'] = target_title
                    self.subscription_data[index]['team'] = target_team
                    if os.path.exists(imgpath) and title != target_title:
                        new_path = os.path.join(project_root, 'res', target_title)
                        os.rename(imgpath, new_path)
                    um.update_subscription(self.subscription_data)
                    self.update_data()
            pass

    def mark_as_watched(self, index):
        """表格菜单 - 标记为看过"""
        um.marked_as_watched(anime_index = self.current_anime, index = index)
        self.update_table(self.current_anime)
        
    def update_table(self, index):
        """更新表格内数据"""
        self.subscription_data = um.load_subscription()
        self.infotable.update(self.subscription_data[index]['New'])
        self.current_anime = index
        
    def contextMenuEvent(self, e):
        """全局右击菜单"""
        menu = RoundMenu(parent=self)
        
        action_update = Action(FIF.SYNC, '检查更新')
        action_update.triggered.connect(self.update_through_web)
        menu.addAction(action_update)
        
        action_addItem = Action(FIF.ADD, '添加订阅')
        action_addItem.triggered.connect(self.add_anime)
        menu.addAction(action_addItem)
        
        menu.addSeparator()
        
        menu.addAction(Action(FIF.CLOSE, '取消'))
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        
    def add_anime(self):
        """全局右击菜单 - 添加订阅"""
        dialog = AddAnimeMessageBox(self.parent())
        if dialog.exec():
            um.subscribe(*dialog.args)
            self.update_data()
            self.update_through_web()
            
        
    def update_through_web(self):
        """右击菜单 - 更新订阅内容（多线程）"""
        self.update_thread = UpdateAction()
        self.update_thread.finnished.connect(self.on_thread_finished)
        self.update_thread.start()
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title='更新中',
            content="正在调取更新内容...",
            target=self,
            parent=self,
            isClosable=True
            )
    
    def on_thread_finished(self):
        """订阅内容更新完毕后"""
        self.update_data()
        self.download_poster_thread = DownloadPosters()
        self.download_poster_thread.finished.connect(self.update_data)
        self.download_poster_thread.finished.connect(lambda: Flyout.create(icon=InfoBarIcon.SUCCESS,
                                                                           title='完成',
                                                                           content="已完成对订阅内容以及海报的更新",
                                                                           target=self.subscribed_anime_page,
                                                                           parent=self,
                                                                           isClosable=True))
        self.download_poster_thread.start()
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title='Downloading',
            content="已完成对订阅的更新，正在下载海报图片...",
            target=self,
            parent=self,
            isClosable=True
            )
    
class UpdateAction(QThread):
    
    finnished = pyqtSignal()
    
    def run(self):
        um.check_update()
        self.finnished.emit()
        
class DownloadPosters(QThread):
    
    finished = pyqtSignal()
    
    def run(self):
        animes = um.load_subscription()
        for anime in animes:
            # 载入需更新的图片链接与文件名
            Urls = anime['imgUrls']
            target_img_names = [url.split("/")[-1] for url in Urls]
            # 检查目标文件夹中是否存在已有的文件名
            imgpath = os.path.join(project_root, 'res', anime['title'])
            
            if not os.path.exists(imgpath):
                os.makedirs(imgpath)
                
            for url, file_name in zip(Urls, target_img_names):
                file_path = os.path.join(imgpath, file_name)
                if os.path.exists(file_path):
                    continue
                else:
                    scraper.download_image(url, file_path)         
                    if anime.get('img', []) == []:
                        anime['img'] = [file_name]
                        um.update_subscription(animes)
                    else:
                        anime['img'].append(file_name)
                        um.update_subscription(animes)
        
        self.finished.emit()

        

        
        



if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    class test(QWidget):
        
        def __init__(self, parent = None) -> None:
            super().__init__(parent)
            self.resize(750, 700)
            self.initUI()
            
        def initUI(self):
            ###
            t = SubscriptionInterface(self)
            ###
            self.show()
        
    app = QApplication(sys.argv)    
    test_window = test()
    sys.exit(app.exec_())

        