'''
Created on Mar 17, 2014

@author: Jordan Guerin
'''

import shutil
import os
'''
Tag info
%01 -> Track Numder
%02 -> Title
%03 -> Artist
%04 -> Year

'''
tag_dict = {
    '%01' : 'tracknumber',
    '%02' : 'title',
    '%03' : 'artist',
    '%04' : 'date'            
}


class tag_to_filename:
    
    def __init__(self, tag_file, pattern = ""):
        self.file = tag_file
        self.pattern = pattern
        self.old_filename = ""
        self.new_filename = ""
        
        self.old_filename = self.file.filename
        self.item = None
        
    def do(self):
        old_path = os.path.join(self.file.parent, self.old_filename)
        new_path = os.path.join(self.file.parent, self.new_filename)
        
        try:
            os.rename(old_path, new_path)
        except:
            return False
        
        
        self.file.update_path(new_path)
        return True
        
    def generate_name(self):
        
        filename = self.pattern
        
        for p in tag_dict:
            ktag = tag_dict[p]
            val = self.file.m_tags[ktag][0]
            
            filename = filename.replace(p, val)
        
        filename = filename + "." + self.file.extension
        
        self.new_filename = filename
