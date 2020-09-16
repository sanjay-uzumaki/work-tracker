import sqlite3
import sys
import data
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
con = sqlite3.connect('data.db')
cur = con.cursor()
import additem
import projdetails
from datetime import date, datetime


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 0, 0)
        self.setWindowTitle("Main")



