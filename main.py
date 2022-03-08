#!/usr/bin/env python

from math import sqrt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from pynput import keyboard

#http://doc.qt.io/qt-5/widget-classes.html#basic-widget-classes[QWidget documentation]

#subclass for QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window()
        self.buttons()
        self.eventListeners()
        
    def window(self):    
        # Window properties
        self.setWindowTitle("MY Calculator")
        self.setMinimumSize(QSize(320,400))
        
    """ Buttons and Layout"""
    def buttons(self):    
        self.grid = QGridLayout()
        
        # QT Buttons and Labels
        self.history = QLabel()
        self.result = QLabel()
        self.input = QLineEdit()
         
        # QT Styles
        self.history.setStyleSheet("background-color: #D5EAFD; font-size: 15px;")        
        self.result.setStyleSheet("background-color: #D5EAFD; font-size: 25px;")       
        self.input.setPlaceholderText("Start calculating already...")
        #self.input.setValidator(QRegularExpressionValidator(QRegularExpression("^[\d () +%/*,-]*$")))
        
        # Defines
        buttons_style = "color: #0C3153; font-size: 15px;"
        
        # Lists
        self.symbols = ["%", "²", "√", "/", "x", "-", "+", "=", "C", ","]
        self.calcSymbols = ["%", "/", "x", "-", "+"]
        self.buttons = []
        self.numbers = []
        self.input_history = []
        
        # Dicts
        self.calcFunctions = {'%':self.mod, '²':self.quadratic, '√':self.mysqrt, '/':self.div, '*':self.mult, 'x':self.mult, '-': self.substract, '+':self.add}
        
        # Variables
        self.first_val = 0
        self.second_val = 0
        self.calc_result = 0
        
        # Filling the lists and styling the GUI        
        for i in range(0, 10):
            x = QPushButton(self.symbols[i]) 
            self.buttons.append(x)
        
        for i in range(0, 10):
            self.buttons[i].setStyleSheet(buttons_style)
        
        for i in range(0, 10):
            x = QPushButton(str(i))
            x.setStyleSheet(buttons_style)
            self.numbers.append(x)
        
        # Adding Widgets
        self.grid.addWidget(self.history, 0, 0, 1, 4)        
        self.grid.addWidget(self.result, 1, 0, 1, 4)
        self.grid.addWidget(self.input, 2, 0, 1, 4)
           
        # Symbols
        self.grid.addWidget(self.buttons[0], 3, 0)
        self.grid.addWidget(self.buttons[1], 3, 1)
        self.grid.addWidget(self.buttons[2], 3, 2)
        self.grid.addWidget(self.buttons[3], 3, 3)
        self.grid.addWidget(self.buttons[4], 4, 3)
        self.grid.addWidget(self.buttons[5], 5, 3)
        self.grid.addWidget(self.buttons[6], 6, 3)
        self.grid.addWidget(self.buttons[7], 7, 3)
        self.grid.addWidget(self.buttons[8], 7, 2)
        self.grid.addWidget(self.buttons[9], 7, 0)
        
        # Numbers
        self.grid.addWidget(self.numbers[0], 7, 1)
        self.grid.addWidget(self.numbers[1], 6, 0)
        self.grid.addWidget(self.numbers[2], 6, 1)
        self.grid.addWidget(self.numbers[3], 6, 2)
        self.grid.addWidget(self.numbers[4], 5, 0)
        self.grid.addWidget(self.numbers[5], 5, 1)
        self.grid.addWidget(self.numbers[6], 5, 2)
        self.grid.addWidget(self.numbers[7], 4, 0)
        self.grid.addWidget(self.numbers[8], 4, 1)
        self.grid.addWidget(self.numbers[9], 4, 2)
    
        self.widg = QWidget()
        self.widg.setLayout(self.grid)
        self.setCentralWidget(self.widg)   
        
        
    
    def eventListeners(self):
        for button in self.buttons:
            button.setCheckable(True)
        
        self.buttons[6].clicked.connect(self.add) 
        self.buttons[7].clicked.connect(self.inputPressed)   
         
        self.input.returnPressed.connect(self.inputPressed)
      
     
    # Stores value when input is pressed / entered   
    def inputPressed(self):
        self.input.textChanged.connect(self.history.setText)
        self.entered_text = self.input.text()
        self.calculate()
        
    
    def calculate(self):  
        splitted = 0  
        entered_sym = ""
        for sym in self.symbols:            
            if sym in self.entered_text:
                if sym == "√":
                    self.second_val = self.entered_text.split(sym)[1]
                    break
                self.first_val = self.entered_text.split(sym)[0]
                self.second_val = self.entered_text.split(sym)[1]
                entered_sym = sym
                splitted = 1
                break
        
        print(entered_sym)  
        print(self.first_val)
        print(self.second_val)  
        
        if splitted == 0:
            self.result.setText(self.entered_text) 
            
        if float(self.second_val) == 0 and entered_sym == "²":
            self.calcFunctions['²']()
            string = str(self.first_val) + entered_sym + " = " + str(self.calc_result)
            self.result.setText(string)
            return
        
        elif self.first_val == 0 and entered_sym == "√":
            self.calcFunctions['√']()
            string = entered_sym + str(self.second_val) + " = " + str(self.calc_result)
            self.result.setText(string)
            return
        
        # if something like √5+1 is entered
        elif self.second_val != 0 and entered_sym == "√":
            self.first_val = self.second_val
            for sym in self.symbols:            
                if sym in self.second_val:
                    self.first_val = self.second_val.split(sym)[0]
                    self.second_val = self.second_val.split(sym)[1]
                    entered_sym = sym
                    splitted = 1
                    break
            
            self.calcFunctions["√"]()
            self.calcFunctions[entered_sym]()            
            string = str(self.first_val) +  entered_sym + str(self.second_val) + " = " + str(self.calc_result)
            self.result.setText(string)
            return       
        
        # if something like 5²+1 is entered
        elif entered_sym == "²" and self.second_val != 0:
            for sym in self.symbols:            
                if sym in self.second_val:
                    self.second_val = self.entered_text.split(sym)[1]
                    entered_sym = sym
                    splitted = 1
                    break
            self.calcFunctions['²']()
            self.calcFunctions[entered_sym]()
            string = str(self.first_val) + " " + entered_sym + " " + str(self.second_val) + " = " + str(self.calc_result)
            self.result.setText(string)            
            return
            
            
        self.calcFunctions[entered_sym]()
       
        string = str(self.first_val) + " " + entered_sym + " " + str(self.second_val) + " = " + str(self.calc_result)
        self.result.setText(string)
        # self.input_history.append
    
    def mod(self):
        self.calc_result = int(self.first_val) % int(self.second_val)
        return self.calc_result
    
    def div(self):
        if int(self.second_val) == 0:
            print("ZeroDivisionError: division by zero")
            self.result.setText("ZeroDivisionError: division by zero")
            return
        self.calc_result = float(self.first_val) / float(self.second_val)
        return self.calc_result
        
    def add(self):
        self.calc_result = float(self.first_val) + float(self.second_val)
        return self.calc_result
    
    def mult(self):
        self.calc_result = float(self.first_val) * float(self.second_val)
        return self.calc_result
    
    def substract(self):
        self.calc_result = float(self.first_val) - float(self.second_val)
        return self.calc_result
    
    def quadratic(self):
        self.first_val = float(self.first_val) ** 2
        
    def mysqrt(self):
        self.first_val = sqrt(float(self.first_val))
        
  
def main():
    import sys
    import numpy as np
    import math
    import random
    
    #(sys.argv) for command line arguments
    app = QApplication([])     

    window = MainWindow()
    window.show()
    
    # Start the event loop.
    app.exec()

if __name__ == "__main__":
    main()
