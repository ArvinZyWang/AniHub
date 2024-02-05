# coding:utf-8

import json
from PyQt5.QtCore import Qt


from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, ComboBox

class AddAnimeMessageBox(MessageBoxBase):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('增加订阅', self)
        self.LineEdit = LineEdit(self)

        self.LineEdit.setPlaceholderText('输入番剧标题')
        self.LineEdit.setClearButtonEnabled(True)
        
        self.teamComboBox = ComboBox(self)
        with open(r'./data/teams.json', "r", encoding='utf-8') as f:
            teams = json.load(f)
            team_names = [key for key in teams][1:]
        self.teamComboBox.addItem(' ')
        self.teamComboBox.addItems(team_names)
        
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.LineEdit)
        self.viewLayout.addWidget(self.teamComboBox)

        # change the text of button
        self.yesButton.setText('确认')
        self.yesButton.clicked.connect(self.emit_args)
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        
        # Disable/Enable button
        self.LineEdit.textChanged.connect(self.validate)
        self.teamComboBox.currentTextChanged.connect(self.validate)


    def validate(self, text:str):
        if text.strip() != '' and self.teamComboBox.text() != ' ':
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
    
    def emit_args(self):
        anime_title = self.LineEdit.text()
        team = self.teamComboBox.text()
        self.args = [anime_title, team]


from PyQt5.QtWidgets import QWidget
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.hBxoLayout = QHBoxLayout(self)
        self.button = PushButton('打开对话框', self)

        self.resize(600, 600)
        self.hBxoLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.button.clicked.connect(self.showDialog)

    def showDialog(self):
        w = AddAnimeMessageBox(self)
        if w.exec():
            print(w.args)
            if w.args == None:
                print('None')


if __name__ == '__main__':
    # enable dpi scale
    from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
    import sys
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()