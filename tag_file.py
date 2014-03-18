from mutagen.mp3 import EasyMP3
from PyQt4 import QtCore
import os

class available_tags:
    
    def __init__(self):
        self.tags = ['date', 'performer', 'tracknumber', 'album', 'genre', 'artist', 'title']

class id3_file:
    
    def __init__(self, file_path):
        self.path = file_path
        self.filename = os.path.basename(self.path)
        self.parent = os.path.dirname(self.path)
        self.extension = self.path.split('.')[-1]
        self.item = None
        self.errors = []
        
        try:
            self.m_tags = EasyMP3(self.path)
            
            #print self.m_tags.keys()
            
        except:
            self.m_tags = None
    
    def contains_errors(self):
        
        if len(self.errors) > 0:
            return True
        return False
    
    def update_path(self, new_filepath):
        self.path = new_filepath
        self.filename = os.path.basename(self.path)
        self.parent = os.path.dirname(self.path)
        self.extension = self.path.split('.')[-1]
        
        if not self.item == None:
            self.item.setText(0, self.filename)
            self.item.setCheckState(0, QtCore.Qt.Unchecked)
        try:
            self.m_tags = EasyMP3(self.path)
            
            #print self.m_tags.keys()
            
        except:
            self.m_tags = None
        
    
    def is_file(self):
        return True
    
    def has_tags(self):
        
        if self.m_tags == None:
            return False
        else:
            return True
    
    def is_handled(self):
        
        if self.extension == 'mp3':
            return True
        
        return False

    def get_album(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["album"][0]
            else:
                return ""
        except:
            self.errors.append("album not readable")
            return ""
    
    def get_genre(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["genre"][0]
            else:
                return ""
        except:
            self.errors.append("genre not readable")
            return ""
    
    def get_track(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["tracknumber"][0]
            else:
                return ""
        except:
            self.errors.append("tracknumber not readable")
            return ""

    def get_artist(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["artist"][0]
            else:
                return ""
        except:
            self.errors.append("artist not readable")
            return ""
    
    def get_date(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["date"][0]
            else:
                return ""
        except:
            self.errors.append("date not readable")
            return ""

    def get_title(self):
        try:
            if not self.m_tags == None:
                return self.m_tags["title"][0]
            else:
                return ""
        except:
            self.errors.append("title not readable")
            return ""
    
    
    def pprint(self):
        print "Path : " + self.path
        print "Filename : " + self.filename
        print "Parent : " + self.parent
        print "Extension : " + self.extension