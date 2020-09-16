import sqlite3
import sys
import data
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
con = sqlite3.connect('data.db')
cur = con.cursor()


class add(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(750, 100, 450, 400)
        self.setWindowTitle("Project Details")
        self.layouts()

        self.show()

    def layouts(self):
        self.vbox=QVBoxLayout()
        self.name=QLineEdit()
        self.name.setPlaceholderText("Please enter the item name")
        self.addbtn=QPushButton("Add Item")
        self.vbox.addWidget(self.name)
        self.vbox.addWidget(self.addbtn)
        self.setLayout(self.vbox)
        self.addbtn.clicked.connect(self.add)
    def add(self):
        data.item_name=self.name.text()
        query = "SELECT Date_Time,Hours FROM project WHERE Name=?"
        projects = cur.execute(query, (data.data_name,)).fetchone()
        item = projects[0]
        item = item.split(',')
        items=int(item[0])
        items=items+1
        item[0]=str(items)
        item.append("{} : -0.0 ".format(data.item_name))
        item=','.join(item)
        query = "UPDATE project set Date_Time =? WHERE Name=?"
        cur.execute(query, (item,data.data_name))
        con.commit()
        data.change=1
        self.close()


