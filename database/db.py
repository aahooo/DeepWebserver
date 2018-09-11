import threading
import os
DATABASE_DIR = "dbFiles"
os.chdir(DATABASE_DIR)


class Database:
    def __init__(self, name = None):
        if name:
            if self.CreateDatabaseFile(name):
                self.CurrentDB = name
                print("DB created successfuly")
            elif self.SelectDatabaseFile(name):
                print("DB selected successfuly")
            else:
                print("Couldn't create DB")

        else:
            print("DB Class instance created")

    def CreateDatabaseFile(self, name):
        if name + ".DF" in os.listdir():
            return False
        open(name + ".DF" , 'w')
        self.CurrentDB = name + ".DF"
        return True

    def SelectDatabaseFile(self, name):
        if name + ".DF" in os.listdir():
            self.CurrentDB = name + ".DF"
            return True
        else:
            return False

    def CreateTable(self , table_name , table_columns ):
        with open(self.CurrentDB , 'a') as DBFile:
            pattern = "<" + table_name + " {"
            for column in table_columns:
                pattern += self._find_type(column) + " " + column + ","
            pattern = pattern[:-1] + "}>"
            
            DBFile.write( pattern.encode("utf-8") )
            pass

    def _find_type(var):
        temp = type(var)
        if temp == str: return "str"
        if temp == int: return "int"
        if temp == float: return "float"
        return 0














    
