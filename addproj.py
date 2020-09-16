import sqlite3
import sys
import data
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
con = sqlite3.connect('data.db')
cur = con.cursor()
from datetime import date, datetime


class add(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(750, 100, 450, 400)
        self.setWindowTitle("Add Project")
        self.layouts()

        self.show()

    def layouts(self):
        self.mainvbox=QVBoxLayout()
        self.layout=[]
        i=0
        while i<11:
            h=QHBoxLayout()
            self.layout.append(h)
            self.mainvbox.addLayout(self.layout[i])
            i=i+1
        print("hi")
        self.widget=[]
        i=0
        while i<11:
            if i==3:
                w=QComboBox()
                self.widget.append(w)
                i=i+1
                continue
            w=QLineEdit()
            self.widget.append(w)
            i=i+1
        print("hi")
        self.name=QLabel("Name:")
        self.client=QLabel("Client:")
        self.place=QLabel("Place:")
        self.type=QLabel("Type:")
        self.starea=QLabel("Site Area:")
        self.btarea=QLabel("Built-up Area:")
        self.floors=QLabel("Floors:")
        self.pkg=QLabel("Package:")
        self.price=QLabel("Price:")
        self.strtdt=QLabel("Start Date:")
        self.enddt=QLabel("End Date:")
        self.layout[0].addWidget(self.name)
        self.layout[1].addWidget(self.client)
        self.layout[2].addWidget(self.place)
        self.layout[3].addWidget(self.type)
        self.layout[4].addWidget(self.starea)
        self.layout[5].addWidget(self.btarea)
        self.layout[6].addWidget(self.floors)
        self.layout[7].addWidget(self.pkg)
        self.layout[8].addWidget(self.price)
        self.layout[9].addWidget(self.strtdt)
        self.layout[10].addWidget(self.enddt)
        i=0
        while i<11:
            self.layout[i].addWidget(self.widget[i])
            i=i+1
        self.setLayout(self.mainvbox)
        self.date = date.today()
        self.date = self.date.strftime("%d/%m/%Y")
        self.widget[9].setText(self.date)
        self.addbtn=QPushButton("Add Project")
        self.hbox=QHBoxLayout()
        self.hbox.addWidget(self.addbtn)
        self.hbox.setAlignment(Qt.AlignCenter)
        self.mainvbox.addLayout(self.hbox)
        self.addbtn.clicked.connect(self.addproj)
        list1=["Residential-House","Residential-Apartment","Commercial"]
        self.widget[3].addItems(list1)
    def addproj(self):
        query = "SELECT * FROM data "
        projects = cur.execute(query).fetchall()
        k = 0
        while k < len(projects):
            if projects[k][1] == self.widget[0].text():
                break
            k = k + 1
        print(k)
        if k == len(projects):
            list=[]
            print("OK")
            i=0
            while i<11:
                if i==3:
                    h=self.widget[3].currentText()
                    list.append(h)
                    i=i+1
                    continue
                h=self.widget[i].text()
                print("OK")
                list.append(h)
                i=i+1
            query = "INSERT INTO data (Name,Client,Place,Type,Site,Built,Floors,Package,Price,Start,End,Total) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10],'0.0'))
            con.commit()
            query = "INSERT INTO project (Name,Date_Time,Hours) VALUES(?,?,?)"
            cur.execute(query, (list[0],"0","0"))
            con.commit()
            print(list)
            self.close()
        else:
            QMessageBox.information(self, "Error", "Project name already exists, please change it")

