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
import blank
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(750, 100, 450, 400)
        self.setWindowTitle("Main")
        self.layouts()
        self.show()
        trayicon = QSystemTrayIcon(QIcon("Logo Short@2x.png"), self)
        trayicon.show()

        menu = QMenu()
        shows = menu.addAction("Show")
        shows.triggered.connect(self.restored)
        showss = menu.addAction("Exit")
        showss.triggered.connect(self.close)
        trayicon.setContextMenu(menu)
    def restored(self):
        self.show()
    def closeEvent(self,event):
        self.hide()
        event.ignore()
    def layouts(self):
        self.mainhbox=QHBoxLayout()
        self.vbox1=QVBoxLayout()
        self.vbox2=QVBoxLayout()
        self.btmlefthbox=QHBoxLayout()
        self.righthbox=QHBoxLayout()
        self.btmrighthbox=QHBoxLayout()
        self.rightvbox=QVBoxLayout()
        self.projlist=QListWidget()
        self.addprojbtn=QPushButton("Add")
        self.dltprojbtn=QPushButton("Delete")
        self.endbtn=QPushButton("End Project")
        self.itemtbl=QTableWidget()
        self.additmbtn=QPushButton("Add Item")
        self.dltitmbtn=QPushButton("Delete Item")
        self.edititmbtn=QPushButton("Edit Item")
        self.startbtn=QPushButton("Start")
        self.stopbtn=QPushButton("Stop")
        self.morebtn=QPushButton("More")
        self.mainhbox.addLayout(self.vbox1)
        self.mainhbox.addLayout(self.vbox2)
        self.vbox1.addWidget(self.projlist)
        self.vbox1.addLayout(self.btmlefthbox)
        self.btmlefthbox.addWidget(self.addprojbtn)
        self.btmlefthbox.addWidget(self.dltprojbtn)
        self.btmlefthbox.addWidget(self.endbtn)
        self.vbox2.addLayout(self.righthbox)
        self.vbox2.addLayout(self.btmrighthbox)
        self.righthbox.addWidget(self.itemtbl)
        self.righthbox.addLayout(self.rightvbox)
        self.rightvbox.addWidget(self.startbtn)
        self.rightvbox.addWidget(self.stopbtn)
        self.rightvbox.addWidget(self.morebtn)
        self.btmrighthbox.addWidget(self.additmbtn)
        self.btmrighthbox.addWidget(self.dltitmbtn)
        self.btmrighthbox.addWidget(self.edititmbtn)
        self.setLayout(self.mainhbox)
        self.projlist.doubleClicked.connect(self.ok)
        self.addprojbtn.clicked.connect(self.addproject)
        self.dltprojbtn.clicked.connect(self.dltproject)
        self.projlist.clicked.connect(self.singleclick)
        self.itemtbl.setColumnCount(2)
        headers=["Item","Hours Worked"]
        self.itemtbl.setHorizontalHeaderLabels(headers)
        self.getprojects()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.getprojects)
        self.additmbtn.clicked.connect(self.additem)
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.start()
        self.timer1.timeout.connect(self.change)
        self.dltitmbtn.clicked.connect(self.deleteitem)
        self.itemtbl.clicked.connect(self.get)
        self.itemtbl.itemChanged.connect(self.ok)
        self.edititmbtn.clicked.connect(self.edititem)
        self.projlist.doubleClicked.connect(self.doubleclick)
        self.startbtn.clicked.connect(self.start)
        self.stopbtn.clicked.connect(self.stop)
        self.endbtn.clicked.connect(self.endproject)
        self.current=None
    def endproject(self):
        if self.projlist.currentItem()==None:
            QMessageBox.information(self, "Error", "Please Select Project to end")
        else:
            self.date = date.today()
            self.date = self.date.strftime("%d/%m/%Y")
            query = "UPDATE data set End =? WHERE Name=?"
            cur.execute(query, (self.date, data.data_name))
            con.commit()
            QMessageBox.information(self, "Info", "Project-{} end date set to {}".format(data.data_name,self.date))
    def start(self):
        if self.itemtbl.currentItem()==None:
            QMessageBox.information(self, "Error", "Please Select Item")
        else :
            if data.start==1:
                QMessageBox.information(self, "Error", "Timer has already been started")
            else:
                data.start_item=data.item_name
                QMessageBox.information(self, "Error", "Timer has been started")
                data.item_name=self.itemtbl.currentItem().text()
                now = datetime.now()
                self.start_time = now.strftime("%H:%M:%S")
                self.start_date = date.today()
                self.start_date = self.start_date.strftime("%d/%m/%Y")
                self.timer2 = QTimer()
                self.timer2.setInterval(60000)
                self.timer2.start()
                self.timer2.timeout.connect(self.addmin)
                self.mins=0
                self.hours=0
                data.start=1
    def addmin(self):
        self.mins=self.mins+1
        if self.mins==60:
            self.mins=0
            self.hours=self.hours+1
    def stop(self):
        if data.start==1:
            self.timer2.stop()
            data.start=0
            QMessageBox.information(self, "Info", "You have worked for {} hours and {} minutes".format(self.hours, self.mins))
            query = "SELECT Date_Time FROM project WHERE Name=?"
            projects = cur.execute(query, (data.data_name,)).fetchone()
            projects = projects[0].split(',')
            items = int(projects[0])
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            i = 1
            while i <= items:
                item = projects[i]
                item = item.split(':')
                if data.start_item == item[0]:
                    item[1]=item[1].split('-')
                    item[1][0]=item[1][0]+" "+self.start_date+" "+str(self.hours)+"."+str(self.mins)
                    item[1][1]=item[1][1].split('.')
                    hours=int(item[1][1][0])+self.hours
                    mins=int(item[1][1][1])+self.mins
                    while mins>60:
                        hours=hours+1
                        mins=mins-60
                    item[1][1]=str(hours)+'.'+str(mins)
                    item[1]='-'.join(item[1])
                    print(item[1])
                    break
                i = i + 1
            item = ':'.join(item)
            print(item)
            projects[i] = item
            projects = ','.join(projects)
            print(projects)
            query = "UPDATE project set Date_Time =? WHERE Name=?"
            cur.execute(query, (projects, data.data_name))
            con.commit()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ###############Total TIme##################
            name = self.projlist.currentItem().text()
            data.data_name = name
            query = "SELECT Date_Time,Hours FROM project WHERE Name=?"
            projects = cur.execute(query, (name,)).fetchone()
            item = (projects[0])
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if item == '0':
                self.itemtbl.setRowCount(0)
            else:
                i = 1
                items = item.split(',')
                self.itemtbl.setRowCount(int(items[0]))
                total_h=0
                total_m=0
                while i <= int(items[0]):
                    itm = items[i].split(':')
                    hours = itm[1].split('-')
                    hours[1] = hours[1].split(".")
                    print(hours[1])
                    total_h=total_h+int(hours[1][0])
                    total_m=total_m+int(hours[1][1])
                    i = i + 1
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                while total_m>60:
                    total_h=total_h+1
                    total_m=total_m-60
                query = "UPDATE data set Total =? WHERE Name=?"
                cur.execute(query, (str(total_h)+" h "+str(total_m)+" m", data.data_name))
                con.commit()

            data.change = 1

        else:
            QMessageBox.information(self, "Error", "You have not started the timer to stop it")
    def edititem(self):
        if self.itemtbl.currentItem() == None:
            QMessageBox.information(self, "Error", "Please Select Item")
        else:
            if self.current==None:
                QMessageBox.information(self, "Error", "Please Double click an item and change it to edit")
            else:
                query = "SELECT Date_Time FROM project WHERE Name=?"
                projects = cur.execute(query, (data.data_name,)).fetchone()
                projects = projects[0].split(',')
                items = int(projects[0])

                i = 1
                while i <= items:
                    item = projects[i]
                    item = item.split(':')
                    if data.item_name == item[0]:
                        item[0]=self.current
                        break
                    i = i + 1
                item=':'.join(item)
                projects[i]=item
                projects = ','.join(projects)
                query = "UPDATE project set Date_Time =? WHERE Name=?"
                cur.execute(query, (projects, data.data_name))
                con.commit()
                data.change = 1
                print(projects)
                QMessageBox.information(self, "Info", "Item Edited")


    def doubleclick(self):
        self.h=projdetails.projdet()
    def get(self):
        data.item_name=self.itemtbl.currentItem().text()
        print(data.item_name)
    def deleteitem(self):
        if self.itemtbl.currentItem() == None:
            QMessageBox.information(self, "Error", "Please Select Item")
        else:
            name=self.itemtbl.currentItem().text()
            query = "SELECT Date_Time FROM project WHERE Name=?"
            projects = cur.execute(query, (data.data_name,)).fetchone()
            projects=projects[0].split(',')
            items=int(projects[0])

            i=1
            while i<=items:
                item=projects[i]
                item=item.split(':')
                if name==item[0]:
                    break
                i=i+1
            items=items-1
            projects[0]=str(items)
            projects.pop(i)
            projects=','.join(projects)
            query = "UPDATE project set Date_Time =? WHERE Name=?"
            cur.execute(query, (projects,data.data_name))
            con.commit()
            data.change=1
            print(projects)
    def change(self):
        if data.change==1:
            name = self.projlist.currentItem().text()
            data.data_name = name
            query = "SELECT Date_Time,Hours FROM project WHERE Name=?"
            projects = cur.execute(query, (name,)).fetchone()
            item = (projects[0])
            if item == '0':
                self.itemtbl.setRowCount(0)
            else:
                i = 1
                items = item.split(',')
                self.itemtbl.setRowCount(int(items[0]))
                while i <= int(items[0]):
                    itm = items[i].split(':')
                    print(itm)
                    hours = itm[1].split('-')
                    self.itemtbl.setItem(i - 1, 0, QTableWidgetItem(itm[0]))
                    hours[1] = hours[1].split(".")
                    hours[1] = hours[1][0] + " h " + hours[1][1] + " m"
                    self.itemtbl.setItem(i - 1, 1, QTableWidgetItem(hours[1]))
                    i = i + 1
            data.change=0
    def ok(self):
        if self.itemtbl.currentItem()!=None:
            self.current = self.itemtbl.currentItem().text()
            print(self.current)
    def addproject(self):
        import addproj
        self.h=addproj.add()
    def getprojects(self):
        index=self.projlist.currentIndex()
        self.projlist.clear()
        query = "SELECT Name FROM data"
        projects = cur.execute(query).fetchall()
        i=0
        while i<len(projects):
            self.projlist.addItem(projects[i][0])
            i=i+1
        self.projlist.setCurrentIndex(index)
    def dltproject(self):
        if self.projlist.currentItem() == None:
            QMessageBox.information(self, "Error", "Please Select Project")
        else:
            name=self.projlist.currentItem().text()
            id=self.getid(name)
            id1=self.getid1(name)
            query = "DELETE FROM data WHERE id=?"
            cur.execute(query, (id,))
            con.commit()
            query = "DELETE FROM project WHERE id=?"
            cur.execute(query, (id1,))
            con.commit()
            QMessageBox.information(self, "Info!!!", "Project has been deleted")
            self.projlist.clear()
            self.getprojects()
    def getid(self,person):
        query = "SELECT Id,Name FROM data"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            if person==employee[1]:
                return employee[0]
    def getid1(self,person):
        query = "SELECT id,Name FROM project"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            if person==employee[1]:
                return employee[0]
    def singleclick(self):
        name = self.projlist.currentItem().text()
        data.data_name = name
        print(name)
        query = "SELECT Date_Time,Hours FROM project WHERE Name=?"
        projects = cur.execute(query,(name,)).fetchone()
        item=(projects[0])
        if item=='0':
            self.itemtbl.setRowCount(0)
        else:
            i=1
            items=item.split(',')
            self.itemtbl.setRowCount(int(items[0]))
            while i<=int(items[0]):
                itm=items[i].split(':')
                print(itm)
                hours=itm[1].split('-')
                self.itemtbl.setItem(i-1, 0, QTableWidgetItem(itm[0]))
                hours[1]=hours[1].split(".")
                hours[1]=hours[1][0]+" h "+hours[1][1]+" m"
                self.itemtbl.setItem(i-1, 1, QTableWidgetItem(hours[1]))
                i=i+1

    def additem(self):
        if self.projlist.currentItem() == None:
            QMessageBox.information(self, "Error", "Please Select Project")
        else:
            name = self.projlist.currentItem().text()
            data.data_name=name
            self.add=additem.add()

App = QApplication(sys.argv)
window = Main()
sys.exit(App.exec())

