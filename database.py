'''
Created on Mar 18, 2014

@author: Jordan Guerin
'''

import sqlite3

class connector:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.connection = None
    
    def open(self):
        if self.connection == None:
            self.connection = sqlite3.connect(self.filepath)
            return self.connection
        else:
            return None
    def get_cursor(self):
        return self.connection.cursor()
    
    def commit(self):
        if not self.connection == None:
            self.connection.commit()
    
    def close(self):
        
        if not self.connection == None:
            self.connection.close()

class table:
    
    def __init__(self, table_name, connector):
        self.name = table_name
        self.connector = connector
        self.structure = ""

    def create_table(self):
        cursor = self.connector.get_cursor()
        cursor.execute(self.structure)

class row:
    def __init__(self, _table):
        self.new = True
        self.table = _table
        
    def is_new(self):
        return self.new
    
    def set_id(self, rid):
        print "id in the universe!!"
    
    def get_id(self):
        return 0
    
    def get_update_query(self):
        return ""
    
    def get_insert_query(self):
        return ""
    
    def get_id_query(self):
        return ""
    
    def from_db(self, rid):
        return

class files_table(table):
    
    def __init__(self, connector):
        table.__init__(self, "files", connector)
        self.structure = """ CREATE TABLE IF NOT EXISTS %s ( file_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, file_name TEXT NOT NULL, full_path TEXT NOT NULL);""" % (self.name)
        self.create_table()
        
    def insert(self, ofile):
        
        if ofile.is_new():
            query = ofile.get_insert_query()

            cursor = self.connector.get_cursor()
            try:
                cursor.execute(query)
            
                query = ofile.get_id_query()
            
                data = cursor.execute(query)

                for row in data:
                    rid = int(row[0])
                    ofile.set_id(rid)
                    break
            
                self.connector.commit()
            except:
                print "*------------------------------------------*"
                print "*SQL Error :"
                print query
                print "*------------------------------------------*"
            
    def update(self, ofile):
        if not ofile.is_new():
            query = ofile.get_update_query()
            
            cursor = self.connector.get_cursor()
            
            cursor.execute(query)
            
            self.connector.commit()
        
        
class file_row(row):
    def __init__(self, connector):
        row.__init__(self, files_table(connector))
        self.file_id = -1
        self.file_name = ""
        self.full_path = ""
    
    def set_id(self, rid):
        self.file_id = rid
        
    def get_id(self):
        return self.file_id
    
    def get_insert_query(self):
        query = """INSERT INTO %s (file_name, full_path) VALUES ('%s','%s')""" % (self.table.name, self.file_name, self.full_path)
        return query
    
    def get_update_query(self):
        query = """UPDATE %s SET file_name = '%s', full_path = '%s' WHERE file_id = %d""" % (self.table.name, self.file_name, self.full_path, self.file_id)
        return query
    
    def get_id_query(self):
        query = """SELECT file_id FROM %s WHERE file_name = '%s' AND full_path = '%s'""" % (self.table.name, self.file_name, self.full_path)
        return query
    
    def from_db(self, file_id):
        query = """SELECT file_id, file_name, full_path FROM %s WHERE file_id = %d""" % (self.table.name, file_id)
        
        data = self.table.connector.get_cursor().execute(query)

        for row in data:
            self.file_id = row[0]
            self.file_name = row[1]
            self.full_path = row[2]
            break
    
    def from_tagfile(self, tag_file):
        self.file_name = tag_file.filename
        self.full_path = tag_file.path
        
    def save(self):
        if self.is_new():
            self.table.insert(self)
        else:
            self.table.update(self)
        

        