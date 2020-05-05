import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import ui
import base1

class Connection(QMainWindow, ui.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.world = base1.ExternalWorld()
        self.begin = True
        self.button_step.clicked.connect(lambda: self.button1_click())
        self.button_contract.clicked.connect(lambda: self.button2_click())
        
    def button1_click(self):
        textbox_animals = [self.textbox_animals_young.text(), self.textbox_animals_adult.text(), self.textbox_animals_old.text()]
        textbox_sold_animals_number = [self.textbox_sold_animals_number_young.text(),self.textbox_sold_animals_number_adult.text(),self.textbox_sold_animals_number_old.text()]
        textbox_sold_animals_price = [self.textbox_sold_animals_young_price.text(),self.textbox_sold_animals_adult_price.text(),self.textbox_sold_animals_old_price.text()]
        self.world.click_button_step(self.textbox_money_capital.text(),textbox_animals,self.textbox_feed.text(),self.textbox_remaining_period.text(),self.textbox_feed_number.text(),self.textbox_feed_price.text(),textbox_sold_animals_number,textbox_sold_animals_price,self.textbox_forfeit.text())
        total = int(self.textbox_money_capital.text())
        total += self.world.farm.animals.animal_capital(self.world.farm.contract.sold_animals_price)
        #animals_number = list(map(int,textbox_animals))
        #animals_price = list(map(int,textbox_sold_animals_price))
        #for i in range(3):
        #    total += animals_price[i]*animals_number[i]
        self.plain_total.setPlainText(str(total))
        self.plainText.appendPlainText(self.world.outstring)
        
    def button2_click(self):
        textbox_animals = [self.textbox_animals_young.text(), self.textbox_animals_adult.text(), self.textbox_animals_old.text()]
        textbox_sold_animals_number = [self.textbox_sold_animals_number_young.text(),self.textbox_sold_animals_number_adult.text(),self.textbox_sold_animals_number_old.text()]
        textbox_sold_animals_price = [self.textbox_sold_animals_young_price.text(),self.textbox_sold_animals_adult_price.text(),self.textbox_sold_animals_old_price.text()]
        self.world.click_button_contract(self.textbox_money_capital.text(),textbox_animals,self.textbox_feed.text(),self.textbox_remaining_period.text(),self.textbox_feed_number.text(),self.textbox_feed_price.text(),textbox_sold_animals_number,textbox_sold_animals_price,self.textbox_forfeit.text())
        self.plainText.appendPlainText(self.world.outstring)
    
app = QApplication(sys.argv)
form = Connection()
form.show()
app.exec()