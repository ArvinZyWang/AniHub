import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

class FileBrowserExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Browser Example')

        # 创建按钮用于触发文件浏览器
        open_button = QPushButton('Open File Browser', self)
        open_button.clicked.connect(self.showDialog)

        self.setGeometry(100, 100, 300, 200)

    def showDialog(self):
        # 打开文件对话框并获取选定的文件路径
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', "D:\Documents\Coding", 'All Files (*);;Text Files (*.txt)')

        if fname:
            print(f'Selected file path: {fname}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = FileBrowserExample()
    example.show()
    sys.exit(app.exec_())
