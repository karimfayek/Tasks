from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUiType
# import os
from PyQt5 import uic , QtCore
from PyQt5.QtGui import QColor# , QPen QPainter,
# from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
from os import path
import sys
from notification import *
import datetime

import pypyodbc


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.username = ''
        username = ''
        uic.loadUi('login.ui', self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin.clicked.connect(self.handleLogin)

    def handleLogin(self):

        if self.textName.text() == 'k' and self.textPass.text() == 'k':
            self.accept()
            Login.username = 'Kariem    '
            print (self.username)
        elif self.textName.text() == 'enjy' and self.textPass.text() == 'enjy':
            self.accept()
        elif self.textName.text() == 'sherok' and self.textPass.text() == 'sherok':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


# FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "Tasks.ui")) FORM_CLASS
timers = [0]


class Thread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        print('hit thread')
        a = MainApp()
        method = getattr(a, 'autoload')
        method()
        self.exec_()


class MainApp(QMainWindow):
    """docstring for main"""
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)# self.setupUi(self)
        uic.loadUi('Tasks.ui', self)
        self.handel_ui()

    def handel_ui(self):
        self.setWindowTitle('Tasks')
        self.btn_load.clicked.connect(self.load)
        self.pushButton_5.clicked.connect(self.insertion)
        self.lineEdit.setPlaceholderText('Enter Task Details')
        self.textEdit.setPlaceholderText('Enter Message  ')
        self.btn_accept.clicked.connect(self.accept)
        self.btn_reply.clicked.connect(self.reply)
        self.btn_send.clicked.connect(self.send)
        self.comboBox_4.currentIndexChanged.connect(self.test)
        self.btn_refuse.clicked.connect(self.refuse)
        #self.load()

    def autoload(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.load)
        timer.start(10000)
        timers[0] = timer

    def update_db(self, query, values):
        connection = pypyodbc.connect('Driver={SQL Server};'
                                      'Server=100.0.0.2;'
                                      'Database=TasksDB;'
                                      'uid=sa;pwd=deveit')
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        connection.close()

    def get_no_tasks(self, query, values):
        connection = pypyodbc.connect('Driver={SQL Server};'
                                      'Server=100.0.0.2;'
                                      'Database=TasksDB;'
                                      'uid=sa;pwd=deveit')
        cursor = connection.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        connection.commit()
        connection.close()
        return results[0][0]

    def sendmsg(self, msg):
        def move2RightBottomCorner(win):
            try:
                screen_geometry = QApplication.desktop().availableGeometry()
                screen_size = (screen_geometry.width(), screen_geometry.height())
                win_size = (win.frameSize().width(), win.frameSize().height())
                x = screen_size[0] - win_size[0] - 10
                y = screen_size[1] - win_size[1] - 10
                win.move(x, y)
            except Exception as e:
                print(e)
        main_window = PopupWindowClass(msg)
        main_window.show()
        move2RightBottomCorner(main_window)

    def popup(self):
        count = self.tableWidget.rowCount()
        item1 = self.tableWidget.item(0, 0)
        i_d1 = item1.text()
        db_no = self.get_no_tasks("SELECT nooftasks FROM count WHERE [user] = ?", [i_d1])
        if db_no < count:
            self.sendmsg('You Have New Task')
            self.update_db("UPDATE count SET nooftasks = ? WHERE [user] = ?", [count, i_d1])
        self.autoload()

    def load(self):
        connection = pypyodbc.connect('Driver={SQL Server};'
                                      'Server=100.0.0.2;'
                                      'Database=TasksDB;'
                                      'uid=sa;pwd=deveit')
        cursor = connection.cursor()
        query = ("SELECT [from] , [To] , [Desc] , Priority , Status , ID , time FROM Tasks WHERE [To] = ? ORDER BY time DESC")
        values = [Login.username]
        cursor.execute(query, values)
        results = cursor.fetchall()
        self.tableWidget.setRowCount(0)

        while results:
            for row_number , row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    # self.tableWidget.item(row_number, column_number).setBackground(QColor('red'))
                    # btn = QPushButton('accept')
                    # self.tableWidget.setCellWidget(row_number, 4, btn)
            # btn.clicked.connect(self.on_click)
            results = cursor.fetchone()
            connection.commit()
            connection.close()

        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 4)
            i_d = item.text()
            if i_d == 'Accepted':
                self.setColortoRow(self.tableWidget, i,0, 102, 0 )
            elif i_d == 'Waiting accept':
                self.setColortoRow(self.tableWidget, i, 255, 128, 0)
                for column in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(i, column).setForeground(QColor('white'))
            elif i_d == 'Refused':
                self.setColortoRow(self.tableWidget, i, 179, 0, 0)
            elif i_d == 'Done':
                self.setColortoRow(self.tableWidget, i, 0, 102, 255)

        # btn.clicked.connect(self.test) red 99, 13, 3
        #self.autoload()
        self.popup()
        #time.sleep(5)
        #self.autoload()

    def setColortoRow(self ,table, rowindex, r,g,b):
        for column in range(self.tableWidget.columnCount()):
            table.item(rowindex, column).setBackground(QColor(r,g,b))

    def reply(self):
        try:
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                cur = currentQTableWidgetItem.row()
                item = self.tableWidget.item(cur, 5)
                i_d = item.text()
                connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=100.0.0.2;'
                                              'Database=TasksDB;'
                                              'uid=sa;pwd=deveit')
                cursor = connection.cursor()
                query = ("SELECT [To] , [Desc] , Priority , Status , ID , progress FROM Tasks WHERE ID = ? ")
                values = [i_d]
                cursor.execute(query, values)
                results = cursor.fetchall()
                self.tableWidget_2.setRowCount(0)

                while results:
                    for row_number, row_data in enumerate(results):
                        self.tableWidget_3.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                            # btn = QPushButton('accept')
                            # self.tableWidget.setCellWidget(row_number, 4, btn)
                    # btn.clicked.connect(self.on_click)
                    results = cursor.fetchone()
                    connection.commit()
                    connection.close()

            self.tabWidget.setCurrentIndex(3)
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            sqlcommand = "SELECT progress  FROM Tasks WHERE ID = ? "
            values2 = [i_d]
            cursor.execute(sqlcommand, values2)
            results = cursor.fetchall()
            progress = int(results[0][0])
            connection.commit()
            connection.close()

            item = self.tableWidget_3.item(0, 4)
            i_d2 = item.text()
            #print(i_d)
            if i_d2 == 'Accepted':
                for column in range(self.tableWidget_3.columnCount()):
                    self.tableWidget_3.item(0, column).setBackground(QColor(0, 102, 0))
            elif i_d2 == 'Waiting accept':
                for column in range(self.tableWidget_3.columnCount()):
                    self.tableWidget_3.item(0, column).setBackground(QColor(255, 128, 0))
            elif i_d2 == 'Refused':
                for column in range(self.tableWidget_3.columnCount()):
                    self.tableWidget_3.item(0, column).setBackground(QColor(153, 0, 0))
            elif i_d2 == 'Done':
                for column in range(self.tableWidget_3.columnCount()):
                    self.tableWidget_3.item(0, column).setBackground(QColor(6, 6, 249))

            self.loadchat(progress, i_d)
        except UnboundLocalError:
            QMessageBox.warning(self, 'Please select a task', 'to reply to task you must select it first from load page ')

    def loadchat(self,progress, i_d):
        connection = pypyodbc.connect('Driver={SQL Server};'
                                      'Server=100.0.0.2;'
                                      'Database=TasksDB;'
                                      'uid=sa;pwd=deveit')
        cursor = connection.cursor()
        sqlcommand= "SELECT [From] , message , status ,time FROM chat WHERE ID = ? ORDER BY time DESC"
        values = [i_d]
        cursor.execute(sqlcommand, values)
        results = cursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        while results:
            for row_number, row_data in enumerate(results):
                self.tableWidget_2.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    #btn = QPushButton('accept')
                    #self.tableWidget.setCellWidget(row_number, 4, btn)
            #btn.clicked.connect(self.on_click)
            results = cursor.fetchone()
            connection.commit()
            connection.close()
        self.spinBox.setValue(progress)

    def send(self):
        try:
            assert self.textEdit.toPlainText() != ''
            now = datetime.datetime.now()
            strf = now.strftime("%Y-%m-%d %H:%M:%S")
            item = self.tableWidget_3.item(0, 4)
            i_d = item.text()
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            sqlcommand = "INSERT INTO chat VALUES (?,?,?,?,?) "
            values = [Login.username, self.textEdit.toPlainText(), self.comboBox_4.currentText(), i_d, strf]
            cursor.execute(sqlcommand, values)
            connection.commit()
            connection.close()
            self.textEdit.setText('')
            self.textEdit.setPlaceholderText('Enter Message  ')

            progress = self.progressBar.value()
            #connection.commit()
            #connection.close()
            self.update_prog(progress, i_d)
            self.update_status(i_d)
            self.loadchat(progress, i_d)
        except AttributeError:
            QMessageBox.warning(self, 'Empty chat ','to reply to task you must select it first from load page ')
        except AssertionError:
            QMessageBox.warning(self, 'no data ', 'please enter message ')

    def refuse(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            cur = currentQTableWidgetItem.row()
            item = self.tableWidget.item(cur ,5)
            i_d = item.text()
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            query = ("UPDATE Tasks SET Status = ? WHERE ID = ?")
            values = ['Refused', i_d]
            cursor.execute(query, values)
            connection.commit()
            connection.close()
            #self.load()
            self.comboBox_4.setCurrentIndex(1)
            self.spinBox.setValue(0)
            self.reply()

    def accept(self):
        try:
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                cur = currentQTableWidgetItem.row()
                item = self.tableWidget.item(cur ,5)
                i_d = item.text()
                connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=100.0.0.2;'
                                              'Database=TasksDB;'
                                              'uid=sa;pwd=deveit')
                cursor = connection.cursor()
                query = ("UPDATE Tasks SET Status = ? WHERE ID = ?")
                values = ['Accepted', i_d]
                cursor.execute(query, values)
                connection.commit()
                connection.close()
                self.load()
        except RuntimeError:
            QMessageBox.information(self,'select one Item', 'select one item')

    def update_prog(self, progress, i_d):
        connection = pypyodbc.connect('Driver={SQL Server};'
                                      'Server=100.0.0.2;'
                                      'Database=TasksDB;'
                                      'uid=sa;pwd=deveit')
        cursor = connection.cursor()
        query = ("UPDATE Tasks SET progress = ? WHERE ID = ?")
        values = [progress, i_d]
        cursor.execute(query, values)
        connection.commit()
        connection.close()

    def returninfo(self):
        print ()


    def insertion(self):

        try :
            assert self.lineEdit.toPlainText() != ''
            now = datetime.datetime.now()
            strf = now.strftime("%Y-%m-%d %H:%M")
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            sqlcommand = "INSERT INTO Tasks VALUES (?,?,?,?,?,?,?)"
            values = [Login.username, self.comboBox.currentText(), self.lineEdit.toPlainText(), self.comboBox_2.currentText(), 'Waiting accept', 0, strf]
            cursor.execute(sqlcommand, values)
            connection.commit()
            connection.close()
            QMessageBox.information(self, 'Submitted', 'Task submitted successfully ')
            self.lineEdit.setText('')
            self.lineEdit.setPlaceholderText('Previous Task Submitted Successfully , Enter New Task Details  ')
        except AssertionError:
            QMessageBox.information(self, 'Empty Task', 'please enter Task details')

    def test(self):
        if self.comboBox_4.currentText() == 'Refuse':
            self.spinBox.setValue(0)
        elif self.comboBox_4.currentText() == 'Done':
            self.spinBox.setValue(100)

    def update_status(self,i_d):
        if self.comboBox_4.currentText() == 'Refuse':
            self.spinBox.setValue(0)
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            query = ("UPDATE Tasks SET status = ? WHERE ID = ?")
            values = ['Refused', i_d]
            cursor.execute(query, values)
            connection.commit()
            connection.close()
        elif self.comboBox_4.currentText() == 'Done':
            self.spinBox.setValue(0)
            connection = pypyodbc.connect('Driver={SQL Server};'
                                          'Server=100.0.0.2;'
                                          'Database=TasksDB;'
                                          'uid=sa;pwd=deveit')
            cursor = connection.cursor()
            query = ("UPDATE Tasks SET status = ? WHERE ID = ?")
            values = ['Done', i_d]
            cursor.execute(query, values)
            connection.commit()
            connection.close()

        else:
            pass


def main():
    app = QApplication(sys.argv)
    login = Login()
    if login.exec_() == QDialog.Accepted:
        window = MainApp()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
