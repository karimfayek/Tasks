from PyQt5 import QtWidgets
# from mainwindow import Ui_MainWindow
        self.username = ''
        uic.loadUi('login.ui', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        '''''
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
'''''
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.username = ''
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        # username = ''
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if self.textName.text() == 'foo' and self.textPass.text() == 'bar':
            self.accept()
            login.username = 'foo'
        elif self.textName.text() == 'enjy' and self.textPass.text() == 'bar':
            self.accept()
            login.username = 'enjy'
        elif self.textName.text() == 'karim' and self.textPass.text() == 'bar':
            self.accept()
            login.username = 'karim'
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        #super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        #self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def printinfo(self):
        print ('hi')


class Window2(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent)

def loaduser():
    if login.username == 'foo':
        window = Window2()
        window.show()
        sys.exit(app.exec_())
    elif login.username == 'karim':
        window = Window2()
        window.show()
        sys.exit(app.exec_())
    elif login.username == 'enjy':
        window = Window()
        window.show()
        sys.exit(app.exec_())



if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        loaduser()

