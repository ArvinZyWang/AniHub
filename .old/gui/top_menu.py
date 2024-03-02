import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from search_interface import SearchInterface
from subscription_interface import SubscriptionInterface
from qfluentwidgets import Pivot


class TopMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dmhy Manager')
        self.setFixedSize(900,700)

        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.searchinterface = SearchInterface(self)
        self.subscriptioninterface = SubscriptionInterface(self)
 

        # add items to pivot
        self.addSubInterface(self.subscriptioninterface, objectName='subscriptionInterface', text='Subscription')
        self.addSubInterface(self.searchinterface, objectName='searchInterface', text='Search')
        
        

        self.vBoxLayout.addWidget(self.pivot, 0)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.subscriptioninterface)
        self.pivot.setCurrentItem(self.subscriptioninterface.objectName())

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = TopMenu()
    w.show()
    app.exec_()