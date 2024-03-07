# coding:utf-8
import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
gui_path = os.path.dirname(file_path)
root_path = os.path.dirname(gui_path)
sys.path.append(file_path)
sys.path.append(root_path)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import NavigationInterface, NavigationItemPosition, qrouter
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar

from search_interface.interface import SearchInterface
from subscription_interface.interface import SubscriptionInterface
from settings_interface.interface import SettingsInterface




class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        defaut_style_L = '<div style="color: black;font-size:20px; font-family: Times New Roman">'
        defaut_style_R = '</div>'
        title = defaut_style_L + 'AniHub <i style="font-size: 14px;"> for Dmhy.org</i>' + defaut_style_R
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        #self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))
        pass


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=False)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.searchInterface = SearchInterface(self)
        self.searchInterface.setObjectName('SearchInterface')
        self.subscriptionInterface = SubscriptionInterface(self)
        self.subscriptionInterface.setObjectName('SubscriptionInterface')
        self.settingsInterface = SettingsInterface(self)
        self.settingsInterface.setObjectName('SettingsInterface')

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()
        self.resize(1000, 700)

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initNavigation(self):
        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)


        # add navigation items to scroll area
        self.addSubInterface(self.searchInterface, FIF.SEARCH, 'Search')
        self.addSubInterface(self.subscriptionInterface, FIF.MEDIA, 'Subscription')

        #self.navigationInterface.addSeparator()

        # add custom widget to bottom
        self.addSubInterface(self.settingsInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)
        
        #!IMPORTANT: don't forget to set the default route key
        qrouter.setDefaultRouteKey(self.stackWidget, self.subscriptionInterface.objectName())

        # set the maximum width
        self.navigationInterface.setExpandWidth(200)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('res/logo.png'))
        self.setWindowTitle('AniHub')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )


    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()