'''
Created on Mar 17, 2014

@author: Jordan Guerin
'''
from PyQt4 import QtGui
import main_frame
import sys

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    #app.setWindowIcon(QtGui.QIcon("assets/icon.png"))
    frame = main_frame.main_frame()
    sys.exit(app.exec_())