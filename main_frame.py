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
        
        self.tree_files.clear()
        self.root = None
        
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
            fc.setFlags(fc.flags() | QtCore.Qt.ItemIsUserCheckable)
            fc.setCheckState(0, QtCore.Qt.Unchecked)
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
            fc.setFlags(fc.flags() | QtCore.Qt.ItemIsUserCheckable)
            fc.setCheckState(0, QtCore.Qt.Unchecked)
            fol.item = fc
            
            parent.addChild(fc)
            
            self.fill_tree_child(fc, fol)
            
    
    def fill_file_widget(self, file_widget, file_data):
        file_widget.setText(1, file_data.get_artist())
        file_widget.setText(2, file_data.get_title())
        file_widget.setText(3, file_data.get_album())
        file_widget.setText(4, file_data.get_track())
        file_widget.setText(5, file_data.get_genre())
        
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
        
        self.gb_fields = QtGui.QGroupBox("File configuration", self)
        
        b_grid = QtGui.QGridLayout()
        b_grid.setSpacing(10)
        
        #filename pattern
        self.lbl_filename = QtGui.QLabel("Filename : ")
        self.tb_filename = QtGui.QLineEdit("%01 - %02")
        
        
        #batch artist update
        self.lbl_artist = QtGui.QLabel("Artist : ")
        self.tb_artist = QtGui.QLineEdit("")
        self.tb_artist.setEnabled(False)
        self.cb_artist = QtGui.QCheckBox()
        self.cb_artist.setChecked(False)
        self.cb_artist.clicked.connect(self.cb_artist_batch)
        
        #batch album update
        self.lbl_album = QtGui.QLabel("Album : ")
        self.tb_album = QtGui.QLineEdit("")
        self.tb_album.setEnabled(False)
        self.cb_album = QtGui.QCheckBox()
        self.cb_album.setChecked(False)
        self.cb_album.clicked.connect(self.cb_album_batch)
        
        #batch year update
        self.lbl_year = QtGui.QLabel("Year : ")
        self.tb_year = QtGui.QLineEdit()
        self.tb_year.setEnabled(False)
        self.cb_year = QtGui.QCheckBox()
        self.cb_year.setChecked(False)
        self.cb_year.clicked.connect(self.cb_year_batch)
        
        #batch genre
        
        self.lbl_genre = QtGui.QLabel("Genre : ")
        self.cbox_genre = QtGui.QComboBox()
        self.cbox_genre.setEditable(False)
        self.cb_genre = QtGui.QCheckBox()
        self.cb_genre.setChecked(False)
        self.cb_genre.clicked.connect(self.cb_genre_batch)
        
        #button
        self.btn_tag_to_name = QtGui.QPushButton("Tag to Filename")
        self.btn_tag_to_name.clicked.connect(self.tag_to_name)
        
        #adding widget to tag grid
        b_grid.addWidget(self.lbl_filename, 0, 0)
        b_grid.addWidget(self.tb_filename, 0, 1)
        
        b_grid.addWidget(self.lbl_artist, 1, 0)
        b_grid.addWidget(self.tb_artist, 1, 1)
        b_grid.addWidget(self.cb_artist, 1, 2)
        
        b_grid.addWidget(self.lbl_album, 2, 0)
        b_grid.addWidget(self.tb_album, 2, 1)
        b_grid.addWidget(self.cb_album, 2, 2)
        
        b_grid.addWidget(self.lbl_year, 3, 0)
        b_grid.addWidget(self.tb_year, 3, 1)
        b_grid.addWidget(self.cb_year, 3, 2)
        
        b_grid.addWidget(self.lbl_genre, 4, 0)
        b_grid.addWidget(self.cbox_genre, 4, 1)
        b_grid.addWidget(self.cb_genre, 4, 2)
        
        b_grid.addWidget(self.btn_tag_to_name, 5, 0)
        
        self.gb_fields.setLayout(b_grid)
        self.gb_fields.setGeometry(10, 30, 400, 210)
        
        self.tree_files = QtGui.QTreeWidget(self)
        self.tree_files.setGeometry(10, 250, 860, 400)
        
        
        columns = QtCore.QStringList()
        
        columns.append("Name")
        columns.append("Artist")
        columns.append("Title")
        columns.append("Album")
        columns.append("Track")
        columns.append("Genre")
        columns.append("Tag Version")
        
        self.tree_files.setColumnCount(columns.count())
        self.tree_files.setHeaderLabels(columns)
        self.tree_files.itemDoubleClicked.connect(self.item_double_clicked)
        self.tree_files.itemClicked.connect(self.item_clicked)
            
        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle("Py ID3 Tools")
        self.show()
        
    def tag_to_name(self):
        
        checked = self.get_checked_items()
        for c in checked:
            print str(c.text(0))
    
    def get_checked_items(self, item_root = None):
        if item_root == None:
            item_root = self.tree_files.topLevelItem(0)
        
        checked = []
        
        ic = item_root.childCount()
        for i in range(ic):
            item = item_root.child(i)

            if item.childCount() > 0:
                items = self.get_checked_items(item)
                for rs in items:
                    checked.append(rs)
            else:
                if item.checkState(0) == QtCore.Qt.Checked:
                    checked.append(item)
        
        return checked
        
    
    def item_clicked(self, item, col):
        
        f = self.root.find_file(item)
        check_state = item.checkState(0)
        if not f == None:
            if f.is_file():
                album = f.get_album()
                artist = f.get_artist()
                date = f.get_date()
                
                self.tb_album.setText(album)
                self.tb_artist.setText(artist)
                self.tb_year.setText(date)
                
                i = self.cbox_genre.findText(f.get_genre())
                
                if not i == -1:
                    self.cbox_genre.setCurrentIndex(i)
                else:
                    self.cbox_genre.addItem(f.get_genre())
                    i = self.cbox_genre.findText(f.get_genre())
                    self.cbox_genre.setCurrentIndex(i)
                
            else:
                if col == 0:
                    self.recursive_checked(f, check_state)
    
    def cb_genre_batch(self):
        
        if self.cb_genre.checkState() == QtCore.Qt.Checked:
            self.cbox_genre.setEditable(True)
        else:
            self.cbox_genre.setEditable(False)   
    
    def cb_year_batch(self):

        if self.cb_year.checkState() == QtCore.Qt.Checked:
            self.tb_year.setEnabled(True)
        else:
            self.tb_year.setEnabled(False)
    
    def cb_album_batch(self):
        
        if self.cb_album.checkState() == QtCore.Qt.Checked:
            self.tb_album.setEnabled(True)
        else:
            self.tb_album.setEnabled(False)
    
    def cb_artist_batch(self):
        
        if self.cb_artist.checkState() == QtCore.Qt.Checked:
            self.tb_artist.setEnabled(True)
        else:
            self.tb_artist.setEnabled(False)
    
    
    def recursive_checked(self, folder, check_state):
        
        for f in folder.folders:
            self.recursive_checked(f, check_state)
            f.item.setCheckState(0, check_state)
        
        for f in folder.files:
            f.item.setCheckState(0, check_state)
        
    
    def item_double_clicked(self, item, col):
        f = self.root.find_file(item)
        
        if not f == None:
            if f.is_file():
                print f.pprint()
                dialog = file_info_dialog(self, f)
            

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    
    frame = main_frame()
    sys.exit(app.exec_())