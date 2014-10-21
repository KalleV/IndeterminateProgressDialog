from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QDialog, QTextEdit)
from PyQt5.QtCore import (Qt, pyqtSignal)
from ui_progress_dialog import Ui_ProgressDialog

class DetailsTextBox(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        self.text_edit = QTextEdit()
        self.text_edit.setFixedHeight(100)
        self.text_edit.setFocusPolicy(Qt.NoFocus)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        
    def set_text(self, text):
        self.text_edit.setPlainText(text)
        
    def text(self):
        return self.text_edit.toPlainText()


class IndeterminateProgressDialog(QDialog):
    canceled = pyqtSignal()

    def __init__(self, window_label, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint)
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self)
        self.set_label_text(window_label)

        self.details_textbox = DetailsTextBox()
        self.ui.gridLayout.addWidget(self.details_textbox, 3, 0, 1, 3)
        self.details_textbox.hide()

        self.ui.details_button.toggled.connect(self._view_details)
        self.ui.cancel_button.clicked.connect(self.close)

    def closeEvent(self, event):
        """Overrides QDialog's close event in order to emit a canceled signal"""
        self.canceled.emit()
        super().closeEvent(event)

    def set_detailed_text(self, text):
        self.details_textbox.set_text(text)
        
    def get_detailed_text(self):
        self.details_textbox.text()
        
    def set_label_text(self, text):
        """Changes the text displayed above the progress bar"""
        self.ui.label.setText(text)
        
    def _view_details(self, visible):
        if visible:
            self.ui.details_button.setText('Hide Details<<')
        else:
            self.ui.details_button.setText('Show Details>>')
        self.details_textbox.setVisible(visible)
