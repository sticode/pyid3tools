'''
Created on Mar 18, 2014

@author: Jordan Guerin
'''

from PyQt4 import QtGui, QtCore
import database

class db_files_frame(QtGui.QMainWindow):
    
    def __init__(self):
        super(db_files_frame, self).__init__()
        
        
        self.init_ui()
        
    def init_ui(self):
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        self.tbl_files = QtGui.QTableWidget(self)
        
        columns = QtCore.QStringList()
        
        columns.append("File Id")
        columns.append("File name")
        columns.append("Full path")
        
        self.tbl_files.setColumnCount(columns.count())
        self.tbl_files.setHorizontalHeaderLabels(columns)
        
        self.setLayout(grid)
        self.setGeometry(100, 100, 600, 800)
        self.setWindowTitle("Database GUI")
        self.show()