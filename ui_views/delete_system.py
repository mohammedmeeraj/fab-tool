from ui.py.delete_system_dialog import Ui_Dialog
from PyQt6.QtWidgets import QDialog,QApplication
import sys
from PyQt6.QtCore import pyqtSignal
class DeleteSystem(QDialog,Ui_Dialog):
    form_data_submitted=pyqtSignal(object,str)
    def __init__(self,systems):
        super().__init__()
        self.setupUi(self)
        self.system_combo.addItems(systems)
        self.system_del_btn.clicked.connect(self.on_submit)
    def on_submit(self):
        system=self.system_combo.currentText()
        self.form_data_submitted.emit(self,system)
