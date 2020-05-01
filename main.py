import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import ui
import base

class example(QMainWindow, ui.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.world = base.external_world()
        self.begin = True
        self.button_step.clicked.connect(lambda: self.button1_click())
        self.button_contract.clicked.connect(lambda: self.button2_click())
        
    def button1_click(self):
        self.world.click_button_step(self.textbox_money_capital.text(),self.textbox_animals.text(),self.textbox_feed.text(),self.textbox_remaining_period.text(),self.textbox_feed_number.text(),self.textbox_feed_price.text(),self.textbox_sold_animals_number.text(),self.textbox_sold_animals_price.text(),self.textbox_forfeit.text())
        total = int(self.textbox_money_capital.text())
        animals_number = list(self.textbox_sold_animals_number.text().split(' '))
        animals_number = list(map(int,animals_number))
        animals_price = list(self.textbox_sold_animals_price.text().split(' '))
        animals_price = list(map(int,animals_price))
        for i in range(3):
            total += animals_price[i]*animals_number[i]
        self.plain_total.setPlainText(str(total))
        self.plainText.appendPlainText(self.world.outstring)
        
    def button2_click(self):
        self.world.click_button_contract(self.textbox_money_capital.text(),self.textbox_animals.text(),self.textbox_feed.text(),self.textbox_remaining_period.text(),self.textbox_feed_number.text(),self.textbox_feed_price.text(),self.textbox_sold_animals_number.text(),self.textbox_sold_animals_price.text(),self.textbox_forfeit.text())
        self.plainText.appendPlainText(self.world.outstring)
    
app = QApplication(sys.argv)
form = example()
form.show()
app.exec()