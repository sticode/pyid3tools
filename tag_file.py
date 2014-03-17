from mutagen.mp3 import EasyMP3
import os

class id3_file:
    
    def __init__(self, file_path):
        self.path = file_path
        self.filename = os.path.basename(self.path)
        self.parent = os.path.dirname(self.path)
        self.extension = self.path.split('.')[-1]
        self.item = None
        
        try:
            self.m_tags = EasyMP3(self.path)
            
            #print self.m_tags.keys()
            
        except:
            self.m_tags = None
            
    def is_handled(self):
        
        if self.extension == 'mp3':
            return True
        
        return False

    def get_album(self):
        if not self.m_tags == None:
            return self.m_tags["album"][0]
        else:
            return ""
    
    def get_track(self):
        if not self.m_tags == None:
            return self.m_tags["tracknumber"][0]
        else:
            return ""

    def get_artist(self):
        if not self.m_tags == None:
            return self.m_tags["artist"][0]
        else:
            return ""

    def get_title(self):
        if not self.m_tags == None:
            return self.m_tags["title"][0]
        else:
            return ""
    
    
    def pprint(self):
        print "Path : " + self.path
        print "Filename : " + self.filename
        print "Parent : " + self.parent
        print "Extension : " + self.extension