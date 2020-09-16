import sqlite3
import sys
import data
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
con = sqlite3.connect('data.db')
cur = con.cursor()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(750, 100, 450, 400)
        self.setWindowTitle("Project Details")
        self.layouts()

        self.show()

    def layouts(self):
        self.mainvbox=QVBoxLayout()
        self.layout=[]
        i=0
        while i<12:
            h=QHBoxLayout()
            self.layout.append(h)
            self.mainvbox.addLayout(self.layout[i])
            i=i+1
        print("hi")
        self.widget=[]
        i=0
        query = "SELECT * FROM data "
        projects = cur.execute(query).fetchall()
        k=0
        while k<len(projects):
            if projects[k][1]==data.data_name:
                break
            k=k+1
        projects=projects[k]

        while i<11:
            if i==3:
                w=QComboBox()
                list1 = ["Residential-House", "Residential-Apartment", "Commercial"]
                w.addItems(list1)
                w.setCurrentText(projects[i+1])
                self.widget.append(w)
                i=i+1
                continue
            w=QLineEdit()
            w.setText(projects[i+1])
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
        self.editbtn=QPushButton("Edit")
        self.savebtn=QPushButton("Save")
        self.layout[11].addWidget(self.savebtn)
        self.savebtn.clicked.connect(self.save)
        print((projects))
    def save(self):
        list = []
        print("OK")
        i = 0
        while i < 11:
            if i == 3:
                h = self.widget[3].currentText()
                list.append(h)
                i = i + 1
                continue
            h = self.widget[i].text()
            print("OK")
            list.append(h)
            i = i + 1
        query = "UPDATE data set Name=?,Client=?,Place=?,Type=?,Site=?,Built=?,Floors=?,Package=?,Price=?,Start=?,End=? WHERE Name=?"
        cur.execute(query, (list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10],data.data_name))
        con.commit()
        query = "UPDATE project set Name=? WHERE Name=?"
        cur.execute(query, (list[0],data.data_name))
        con.commit()
        QMessageBox.information(self, "Info", "Project-{} is edited".format(data.data_name))
        data.change=1
        self.close()
