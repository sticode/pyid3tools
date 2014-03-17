'''
Created on Mar 17, 2014

@author: Jordan Guerin
'''

import tag_file
import os

class folder:
    
    def __init__(self, folder_name):
        self.name = folder_name
        self.files = []
        self.folders = []
        self.item = None
    
    def is_file(self):
        return False

    def find_file(self, item):
        
        for f in self.files:
            if f.item == item:
                return f
        
        for f in self.folders:
            if f.item == item:
                return f
            
            rs = self.walk(f, item)
            if not rs == None:
                return rs
            
        return None
            
    def walk(self, parent, item):
        
        for f in parent.files:
            if f.item == item:
                return f
        
        for f in parent.folders:
            if f.item == item:
                return f
            
            rs = self.walk(f, item)
            if not rs == None:
                return rs
        
        return None

    def add_file(self, file):
        self.files.append(file)
    
    def add_folder(self, folder):
        self.folders.append(folder)
        
    def is_empty(self):
        
        if len(self.files) == 0:
            if len(self.folders) == 0:
                return True
            
        return False

class folder_scanner:
    
    def __init__(self, folder_path):
        self.path = folder_path
        self.root = folder(folder_path)
    
    
    def read_root(self):
        
        files = os.listdir(self.path)
        
        for f in files:
            fpath = os.path.join(self.path, f)
            if os.path.isdir(fpath):
                nfolder = folder(f)
                self.root.add_folder(nfolder)
                self.read_folder(nfolder, f)
                
            elif os.path.isfile(fpath):
                self.read_file(self.root, f)
    
    
    def read_folder(self, container, folder_name):

        fpath = os.path.join(self.path, folder_name)
        
        files = os.listdir(fpath)
        
        for f in files:
            
            _fpath = os.path.join(fpath, f)
            
            if os.path.isdir(_fpath):
                nfolder = folder(f)
                container.add_folder(nfolder)
                
                relp = os.path.join(folder_name, f)
                self.read_folder(nfolder, relp)
                
            elif os.path.isfile(_fpath):
                self.read_file(container, f, folder_name)
        
    
    def read_file(self, container, file_name, parent = None):
        ftag = None
        
        if parent == None:    
            fpath = os.path.join(self.path, file_name)

            ftag = tag_file.id3_file(fpath)
            
        else:
            fpath = os.path.join(self.path, parent, file_name)
            
            ftag = tag_file.id3_file(fpath)
            
        if not ftag == None:
            if ftag.is_handled():
                container.add_file(ftag)
            