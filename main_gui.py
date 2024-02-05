from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
gui_dir = os.path.abspath(os.path.join(current_dir, 'gui'))
sys.path.append(gui_dir)
from gui.top_menu import TopMenu
from qfluentwidgets import FluentIcon as FIF, Icon


QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication(sys.argv)
window = TopMenu()
window.setWindowTitle('Dmhy')
window.setWindowIcon(Icon(FIF.MEDIA))
window.show()
sys.exit(app.exec_())
