'''
Created on Mar 17, 2014

@author: Jordan Guerin
'''
import os


class genre_list:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.genres = []
        
        if os.path.exists(self.filepath):
            self.load()
            
    def load(self):
        
        fp = open(self.filepath, 'r')
        
        lines = fp.readlines()
        
        fp.close()
        
        for l in lines:
            l = l.strip("\n")
            self.genres.append(l)
    
    def save(self):
        
        fp = open(self.filepath, 'w')
        
        for g in self.genres:
            fp.write(g+"\n")
            
        fp.close()
    
    
if __name__ == '__main__':
    
    #generating genres file
    
    genres = genre_list("genres.list")
    
    fp = open("tmp.genre", 'r')
    
    lines = fp.readlines()
    
    for l in lines:
        l = l.strip("\n")
        l = l.strip("\r")
        l = l.strip(" ")
        l = l.split(" = ")[1]
        genres.genres.append(l)
        
    fp.close()
    
    genres.save()
    