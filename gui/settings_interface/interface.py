import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)


from lib.models.settings import Settings
from lib.models.server import Server

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame, QSpacerItem

from qfluentwidgets import SmoothScrollArea, SubtitleLabel, ComboBox

class SettingsInterface(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = Settings()
        self.initUi()
        
    def initUi(self):
        # 创建一个滚动区域
        scrollArea = SmoothScrollArea(self)
        scrollArea.setFrameStyle(QFrame.NoFrame)
        scrollArea.setWidgetResizable(True)  # 允许滚动区域中的小部件调整大小

        # 创建一个容器小部件和布局来保存设置项
        settingsContainer = QWidget()
        rootLayout = QVBoxLayout(settingsContainer)
        rootLayout.setAlignment(Qt.AlignTop)
        rootLayout.setContentsMargins(30,45,30,30)

        # 服务器选择：
        promptLabel = SubtitleLabel('选择更新服务器')
        promptLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        rootLayout.addWidget(promptLabel)
        self.serverComboBox = ComboBox(self)
        self.serverComboBox.addItems([
            'Dmhy.org -- 主站, 但需要代理',
            'onekuma.cn -- 镜像站, 但无法载入图片',
            'waaa.moe -- 镜像站, 和主站相同, 但有反爬机制'
        ])
        currentServer = self.settings.server
        currentIndex = [server.value for server in Server].index(currentServer)
        self.serverComboBox.setCurrentIndex(currentIndex)
        self.serverComboBox.currentIndexChanged.connect(lambda index:self.onServerChanged(index))
        self.serverComboBox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        serverLayout = QHBoxLayout()
        serverLayout.addWidget(self.serverComboBox)
        serverLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        rootLayout.addLayout(serverLayout)
        
        # 设置滚动区域的小部件
        scrollArea.setWidget(settingsContainer)

        # 创建主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(scrollArea)
        self.setLayout(mainLayout)
        
    def onServerChanged(self, index):
        self.settings.server = [server.value for server in Server][index]
        self.settings.save()


if __name__ == "__main__":
    #settings = Settings()
    #settings.save()
    pass