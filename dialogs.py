'''
Created on Mar 17, 2014

@author: Jordan Guerin
'''
from PyQt4 import QtGui, QtCore
import file_edit

class file_rename_dialog(QtGui.QDialog):
    
    def __init__(self, parent, pattern):
        super(file_rename_dialog, self).__init__(parent)
        self.pattern = pattern
        self.files = []
        self.ops = []
        self.init_ui()
    
    def init_ops(self):
        
        for f in self.files:
            
            if f.is_file():
                op = file_edit.tag_to_filename(f, self.pattern)
                op.generate_name()
                self.ops.append(op)
        
        self.fill_table()
        
    def fill_table(self):
        ir = 0
        
        for o in self.ops:
            self.tbl_renames.insertRow(ir)
            
            o.item = ir
            cell = QtGui.QTableWidgetItem()
            cell.setText(o.old_filename)
            cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.tbl_renames.setItem(ir, 0, cell)
            
            cell = QtGui.QTableWidgetItem()
            cell.setText(o.new_filename)
            cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.tbl_renames.setItem(ir, 1, cell)
            
            cell = QtGui.QTableWidgetItem()
            cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            
            self.tbl_renames.setItem(ir, 2, cell)
            
            ir = ir + 1
        
    def init_ui(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        self.tbl_renames = QtGui.QTableWidget(self)
        
        self.tbl_renames.setRowCount(0)
        self.tbl_renames.setColumnCount(3)
        self.tbl_renames.setHorizontalHeaderLabels(['Old Filename', 'New Filename', 'Done'])
        #self.tbl_renames.setGeometry(10, 10, 330, 480)
        
        grid.addWidget(self.tbl_renames, 0, 0, 4, 4)
        
        self.btn_rename = QtGui.QPushButton("Rename")
        self.btn_rename.clicked.connect(self.do_ops)
        
        self.btn_close = QtGui.QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        
        grid.addWidget(self.btn_rename, 4, 0)
        grid.addWidget(self.btn_close, 4, 3)
        
        self.setLayout(grid)
        self.setGeometry(100, 100, 350, 500)
        self.setWindowTitle("Rename preview")
        self.show()
        
    def do_ops(self):
        
        for o in self.ops:
            ir = o.item
            if not ir == None:
                item = self.tbl_renames.item(ir, 2)
                
                if o.do():
                    item.setText("Done !")
                else:
                    item.setText("Error !")

class file_info_dialog(QtGui.QDialog):
    
    def __init__(self, parent, file):
        super(file_info_dialog, self).__init__(parent)
        self.file = file
        self.init_ui()
    
    def init_ui(self):
        
        self.lbl_filename = QtGui.QLabel("Path : " + self.file.path)
        
        self.btn_add_tag = QtGui.QPushButton("Add Tag...")
        
        self.btn_remove_tag = QtGui.QPushButton("Remove tag")
        
        self.btn_close = QtGui.QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        
        self.tbl_tags = QtGui.QTableWidget()
        
        columns = QtCore.QStringList()
        
        columns.append("Name")
        columns.append("Value")
        
        self.tbl_tags.setColumnCount(2)
        self.tbl_tags.setHorizontalHeaderLabels(columns)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.lbl_filename, 0, 0)
        grid.addWidget(self.tbl_tags, 2, 0, 4, 4)
        
        grid.addWidget(self.btn_add_tag, 7, 1)
        grid.addWidget(self.btn_remove_tag, 7, 2)
        grid.addWidget(self.btn_close, 7, 3)
        
        self.setLayout(grid)
        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle("File Information : " + self.file.filename)
        self.show()
        
        self.fill_tags()
        
    def fill_tags(self):
        
        tags = self.file.m_tags
        #self.tbl_tags.insertColumn(2)
        
        if not tags == None: 
            ri = 0 
            print tags.keys()
            for k in self.file.m_tags.keys():
                self.tbl_tags.insertRow(ri)
                #self.tbl_tags.setRowCount(ri)
                cell = QtGui.QTableWidgetItem(k)
                cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.tbl_tags.setItem(ri, 0, cell)
                
                cell = QtGui.QTableWidgetItem(tags[k][0])
                cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
                self.tbl_tags.setItem(ri, 1, cell)
                
                ri = ri + 1
                    
        