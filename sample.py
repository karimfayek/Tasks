import sys
from PyQt5 import QtCore, QtWidgets
import index
class Thread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        thread_func()
        #index.MainApp.autoload(self)
        self.exec_()

timers = []

def thread_func():
    #print("Thread works")
    timer = QtCore.QTimer()
    timer.timeout.connect(timer_func)
    timer.start(1000)
    timers.append(timer)
    print[timers]

def timer_func():
    print("Timer works")
    #print [timers]

app = QtWidgets.QApplication(sys.argv)
thread_instance = Thread()
thread_instance.start()
sys.exit(app.exec_())