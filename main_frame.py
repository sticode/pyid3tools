from PyQt4 import QtGui, QtCore
import dialogs
import scanner
import os
import tools

class icon:
    def __init__(self, extension, fpath):
        self.extension = extension
        self.path = fpath
        self.icon = QtGui.QIcon(fpath)
        

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
        self.init_tree_columns()
        self.root = None
        
        fpath = QtGui.QFileDialog.getExistingDirectory(self, "Choose a folder")
        
        fpath = str(fpath)
        
        if os.path.exists(fpath):   
            fscan = scanner.folder_scanner(fpath)
            
            fscan.read_root()
            
            self.root = fscan.root
            
            self.fill_tree()
        else:
            QtGui.QMessageBox.warning(self, "Warning !","Invalid folder selected")
    
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
        try:
            file_widget.setText(1, file_data.get_artist())
            file_widget.setText(2, file_data.get_title())
            file_widget.setText(3, file_data.get_album())
            file_widget.setText(4, file_data.get_track())
            file_widget.setText(5, file_data.get_genre())
        except:
            file_widget.setText(6, "Error Reading Tag")
            print "error reading tag"
        
        file_widget.setFlags(file_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
        file_widget.setCheckState(0, QtCore.Qt.Unchecked)
        
    def check_all_items(self):
        self.recursive_checked(self.root, QtCore.Qt.Checked)
    
    def uncheck_all_items(self):
        self.recursive_checked(self.root, QtCore.Qt.Unchecked)
    
    def name_to_tag(self):
        
        print "TO DO"
        artist = None
        date = None
        album = None
        genre = None
        
        if self.cb_artist.checkState() == QtCore.Qt.Checked:
            artist = str(self.tb_artist.text())
        
        if self.cb_year.checkState() == QtCore.Qt.Checked:
            date = str(self.tb_year.text())
        
        if self.cb_album.checkState() == QtCore.Qt.Checked:
            album = str(self.tb_album)
        
        if self.cb_genre.checkState() == QtCore.Qt.Checked:
            genre = str(self.cbox_genre.currentText())
        
        
        
        
    def init_menu(self):
        self.menu =  self.menuBar()
        
        #file menu
        self.open_folder = QtGui.QAction("Open folder...", self)
        self.open_folder.triggered.connect(self.open_folder_dialog)
        
        self.close_apps = QtGui.QAction("Quit", self)
        self.close_apps.triggered.connect(self.close)
        
        #edit menu
        self.edit_check_all = QtGui.QAction("Check all", self)
        self.edit_check_all.triggered.connect(self.check_all_items)
        
        self.edit_uncheck_all = QtGui.QAction("Uncheck all", self)
        self.edit_uncheck_all.triggered.connect(self.uncheck_all_items)

        
        self.file_menu = self.menu.addMenu("&File")
        
        self.edit_menu = self.menu.addMenu("&Edit")
        
        
        self.file_menu.addAction(self.open_folder)
        self.file_menu.addAction(self.close_apps)
        
        self.edit_menu.addAction(self.edit_check_all)
        self.edit_menu.addAction(self.edit_uncheck_all)
    
    def init_ui(self):
        
        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))
        
        self.init_menu()
        
        self.gb_fields = QtGui.QGroupBox("File configuration", self)
        
        b_grid = QtGui.QGridLayout()
        b_grid.setSpacing(10)
        
        #filename pattern
        self.lbl_filename = QtGui.QLabel("Filename : ")
        self.tb_filename = QtGui.QLineEdit("%01 - %02")
        self.btn_pattern_help = QtGui.QPushButton("Help ?")
        self.btn_pattern_help.clicked.connect(self.dialog_pattern_help)
        
        
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
        
        self.btn_name_to_tag = QtGui.QPushButton("Filename to tag")
        self.btn_name_to_tag.clicked.connect(self.name_to_tag)
        
        #adding widget to tag grid
        b_grid.addWidget(self.lbl_filename, 0, 0)
        b_grid.addWidget(self.tb_filename, 0, 1)
        b_grid.addWidget(self.btn_pattern_help, 0, 2)
        
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
        
        genres = tools.genre_list('genres.list')
        for g in genres.genres:
            self.cbox_genre.addItem(g)
        
        b_grid.addWidget(self.btn_tag_to_name, 5, 0)
        b_grid.addWidget(self.btn_name_to_tag, 5, 1)
        
        self.gb_fields.setLayout(b_grid)
        self.gb_fields.setGeometry(10, 30, 400, 210)
        
        self.tree_files = QtGui.QTreeWidget(self)
        self.tree_files.setGeometry(10, 250, 860, 400)
        
        self.tree_files.itemDoubleClicked.connect(self.item_double_clicked)
        self.tree_files.itemClicked.connect(self.item_clicked)
            
        self.init_tree_columns()
            
        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle("Py ID3 Tools")
        self.show()
        
    def init_tree_columns(self):
        columns = QtCore.QStringList()
        
        columns.append("Name")
        columns.append("Artist")
        columns.append("Title")
        columns.append("Album")
        columns.append("Track")
        columns.append("Genre")
        columns.append("Other info")
        #columns.append("Tag Version")
        
        self.tree_files.setColumnCount(columns.count())
        self.tree_files.setHeaderLabels(columns)
        
        
    def tag_to_name(self):
        
        checked = self.get_checked_items()
        
        if len(checked) == 0:
            return
        
        files = []
        for c in checked:
            
            f = self.root.find_file(c)
            
            if not f == None:
                files.append(f)
                
        
        dialog = dialogs.file_rename_dialog(self, str(self.tb_filename.text()))
        dialog.files = files
        dialog.init_ops()
        
    def dialog_pattern_help(self):

        dialogs.pattern_help_dialog(self)
 
    def get_checked_items(self, item_root = None):
        if item_root == None:
            item_root = self.tree_files.topLevelItem(0)
        
        if item_root == None:
            return []
        
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
                #print f.pprint()
                dialogs.file_info_dialog(self, f)

if __name__ == "__main__":
    print "You need to use 'pyid3tools.py' to launch this application..."
            