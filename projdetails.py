import sqlite3
import sys
from PyQt5.QtCore import QSize, Qt, QTimer

from PyQt5 import QtWidgets

import data
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
con = sqlite3.connect('data.db')
cur = con.cursor()
import editproj

class projdet(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 2000,1000)
        self.setWindowTitle("Project Details")
        self.layouts()

        self.showMaximized()

    def layouts(self):
        self.details=QTableWidget()
        self.details.maximumSize()
        self.details.resize(QSize(2000,1000))
        self.details.setColumnCount(12)
        h=["Name","Client","Place","Type","Site Area","Built-up Area","Floors","Package","Price","Start Date","End Date","Total Time"]
        self.details.setHorizontalHeaderLabels(h)
        self.details.setItem(0, 0, QTableWidgetItem("First Item"))
        query = "SELECT * FROM data "
        projects = cur.execute(query).fetchall()
        print((projects))
        self.details.setRowCount(len(projects))
        i=0
        while i<len(projects):
            j=0
            while j<12:
                self.details.setItem(i,j, QTableWidgetItem(projects[i][j+1]))
                j=j+1
            i=i+1
        self.vbox=QVBoxLayout()
        self.editbtn=QPushButton("Edit")
        self.vbox.addWidget(self.details)
        self.vbox.addWidget(self.editbtn)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignCenter)
        self.editbtn.clicked.connect(self.editproject)
        self.details.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.get)
    def get(self):
        if data.change==1:
            self.details.clear()
            h = ["Name", "Client", "Place", "Type", "Site Area", "Built-up Area", "Floors", "Package", "Price",
                 "Start Date", "End Date", "Total Time"]
            self.details.setHorizontalHeaderLabels(h)
            query = "SELECT * FROM data "
            projects = cur.execute(query).fetchall()
            print((projects))
            self.details.setRowCount(len(projects))
            i = 0
            while i < len(projects):
                j = 0
                while j < 12:
                    self.details.setItem(i, j, QTableWidgetItem(projects[i][j + 1]))
                    j = j + 1
                i = i + 1
            data.change=0
    def editproject(self):
        if self.details.currentItem()==None:
            QMessageBox.information(self, "Error", "You have not selected any project!!!!")
        else:
            data.data_name=self.details.currentItem().text()
            query = "SELECT * FROM data "
            projects = cur.execute(query).fetchall()
            k = 0
            while k < len(projects):
                if projects[k][1] == data.data_name:
                    break
                k = k + 1
            if k==len(projects):
                QMessageBox.information(self, "Error", "Please select a project name only!!!!")
            else:
                self.e=editproj.Main()



