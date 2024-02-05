import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel,
                             QScrollArea, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtCore import Qt

current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Selector')

        # 创建布局
        main_layout = QVBoxLayout()

        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # 创建包含图片的小部件
        scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(scroll_content)

        # 创建水平布局
        self.image_layout = QHBoxLayout(scroll_content)
        scroll_content.setLayout(self.image_layout)

        # 添加滚动区域到主布局
        main_layout.addWidget(scroll_area)

        # 创建按钮用于打开文件对话框
        open_button = QPushButton('Open Directory', self)
        open_button.clicked.connect(self.showDialog)
        main_layout.addWidget(open_button)

        self.showImages()
        self.setLayout(main_layout)

    def showDialog(self):
        # 打开文件夹对话框并获取选定的文件夹路径
        directory = QFileDialog.getExistingDirectory(self, 'Open Directory', '/path/to/your/directory')

        if directory:
            # 清空之前的图片
            self.clearImages()

            # 显示选定目录下的所有图片
            self.showImages(directory)

    def showImages(self, directory = os.path.join(project_root, 'res', "It's MyGO")):
        # 获取目录下所有的图片文件
        image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # 显示图片
        for file in image_files:
            filepath = os.path.join(directory, file)
            pixmap = QPixmap(filepath)

            # 创建标签以显示图片
            image_label = QLabel(self)
            image_label.setPixmap(pixmap.scaledToWidth(100))  # 缩放图片以适应布局
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            image_label.setAlignment(Qt.AlignTop)
            image_label.setToolTip(filepath)

            # 将图片添加到水平布局
            self.image_layout.addWidget(image_label)
            
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)

    def clearImages(self):
        # 清空之前的图片
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    selector = ImageSelector()
    selector.show()
    sys.exit(app.exec_())