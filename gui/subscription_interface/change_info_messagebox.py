from anime_card import SubscribedAnime
from add_anime_messagebox import AddAnimeMessageBox

class ChangeInfoMessagebox(AddAnimeMessageBox):
    
    def __init__(self, parent, editedAnime:SubscribedAnime):
        super().__init__(parent)
        self.titleLabel.setText("编辑订阅")
        self.editedAnime = editedAnime
        
        self.LineEdit.setPlaceholderText(self.editedAnime.title)
        
        self.teamComboBox.setCurrentText(self.editedAnime.team)
        
    def validate(self, text: str):
        super().validate(text)
        if self.teamComboBox.text() == self.editedAnime:
            self.yesButton.setEnabled(False)
        
