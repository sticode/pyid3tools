from PyQt4 import QtGui, QtCore
import scanner
import sys

class icon:
    def __init__(self, extension, fpath):
        self.extension = extension
        self.path = fpath
        self.icon = QtGui.QIcon(fpath)

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
                    
        
        

class main_frame(QtGui.QMainWindow):
    
    def __init__(self):
        super(main_frame, self).__init__()
        
        self.init_ui()
        self.root = None
        self.audio_icons = []
        self.folder_icon = None
        self.load_icons()
        
    def load_icons(self):
        
        self.folder_icon = QtGui.QIcon("assets/folder.png")
        
        i = icon('mp3', 'assets/mp3.png')
        
        self.audio_icons.append(i)
    
    def get_audio_icon(self, extension):
        
        for i in self.audio_icons:
            if i.extension == extension:
                return i.icon
            
        return None
    
    def open_folder_dialog(self):
        
        fpath = QtGui.QFileDialog.getExistingDirectory(self, "Choose a folder")
        
        fscan = scanner.folder_scanner(str(fpath))
        
        fscan.read_root()
        
        self.root = fscan.root
        
        self.fill_tree()
    
    def fill_tree(self):
        
        tree_root = QtGui.QTreeWidgetItem()
        tree_root.setText(0, self.root.name)
        self.tree_root = tree_root
        
        self.root.item = tree_root
        
        for fil in self.root.files:
            
            fc = QtGui.QTreeWidgetItem()
            fc.setText(0, fil.filename)
            fc.setIcon(0, self.get_audio_icon('mp3'))

            fil.item = fc
            self.fill_file_widget(fc, fil)
            tree_root.addChild(fc)
        
        for fol in self.root.folders:
            
            fc = QtGui.QTreeWidgetItem()
            fc.setText(0, fol.name)
            fc.setIcon(0, self.folder_icon)
            
            fol.item = fc
            
            self.fill_tree_child(fc, fol)
            
            tree_root.addChild(fc)
            
        self.tree_files.addTopLevelItem(tree_root)
    
    def fill_tree_child(self, parent, folder):
        
        for fil in folder.files:
            
            fc = QtGui.QTreeWidgetItem()
            fc.setText(0, fil.filename)
            fc.setIcon(0, self.get_audio_icon('mp3'))
            parent.addChild(fc)
            fil.item = fc
            self.fill_file_widget(fc, fil)
            
        for fol in folder.folders:
            
            fc = QtGui.QTreeWidgetItem()
            fc.setText(0, fol.name)
            fc.setIcon(0, self.folder_icon)
            
            fol.item = fc
            
            parent.addChild(fc)
            
            self.fill_tree_child(fc, fol)
            
    
    def fill_file_widget(self, file_widget, file_data):
        file_widget.setText(1, file_data.get_artist())
        file_widget.setText(2, file_data.get_title())
        file_widget.setText(3, file_data.get_album())
        file_widget.setText(4, file_data.get_track())
        
        file_widget.setFlags(file_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
        file_widget.setCheckState(0, QtCore.Qt.Unchecked)
        
    
    def init_menu(self):
        self.menu =  self.menuBar()
        
        self.open_folder = QtGui.QAction("Open folder...", self)
        self.open_folder.triggered.connect(self.open_folder_dialog)
        
        self.file_menu = self.menu.addMenu("&File")
        
        self.file_menu.addAction(self.open_folder)
    
    def init_ui(self):
        
        
        self.init_menu()
        
        self.tree_files = QtGui.QTreeWidget(self)
        self.tree_files.setGeometry(10, 20, 600, 400)
        
        
        columns = QtCore.QStringList()
        
        columns.append("Name")
        columns.append("Artist")
        columns.append("Title")
        columns.append("Album")
        columns.append("Track")
        columns.append("Tag Version")
        
        self.tree_files.setColumnCount(columns.count())
        self.tree_files.setHeaderLabels(columns)
        self.tree_files.itemDoubleClicked.connect(self.open_file_info_dialog)
            
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle("Py ID3 Tools")
        self.show()
        
    def open_file_info_dialog(self, item, col):
        
        f = self.root.find_file(item)
        
        if not f == None:
            print f.pprint()
            dialog = file_info_dialog(self, f)
            

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    
    frame = main_frame()
    sys.exit(app.exec_())