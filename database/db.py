import threading
import os
import hashlib
DATABASE_DIR = "dbFiles"
os.chdir(DATABASE_DIR)


class Database:
    def __init__(self, name = None):
        if name:
            if self.CreateDatabaseFile(name):
                print("DB created successfuly")
            elif self.SelectDatabaseFile(name):
                print("DB selected successfuly")
            else:
                print("Couldn't create DB")

        else:
            print("DB Class instance created")

    def CreateDatabaseFile(self, name):
        if name + ".df" in os.listdir():
            return False
        open(name + ".df" , 'w')
        self.CurrentDB = name + ".df"
        return True

    def SelectDatabaseFile(self, name):
        if name + ".df" in os.listdir():
            self.CurrentDB = name + ".df"
            return True
        else:
            return False

    def CreateTable(self , table_name , table_columns ):
        table_signature = "{}>".format(table_name)
        for column in table_columns:
            table_signature += self._find_type(column)
            table_signature += " "
            table_signature += column
            table_signature += ","
        table_signature = table_signature[:-1]
        table_signature = table_signature.encode("utf-8")
        table_signature = hashlib.sha256(table_signature).hexdigest()[:10]
        
        with open(self.CurrentDB , 'a') as DBFile:
            pattern = "<" + table_name + " {"
            for column in table_columns:
                pattern += self._find_type(column) + " " + column + ","
            pattern = pattern[:-1] + "}"
            pattern += table_signature
            pattern += ">"
            pattern += "\n"
            
            DBFile.write( pattern )
            pass

    def _find_type(self,var):
        temp = type(var)
        if temp == str: return "str"
        if temp == int: return "int"
        if temp == float: return "float"
        return 0

    def ReadTables(self):
        tbl_list = list()
        with open(self.CurrentDB , "r") as dbfile:
            temp = dbfile.readlines(1)
            while len(temp)!=0:
                temp = temp[0].replace("\n","")
                if temp[0]=="<":
                    tbl_name = temp.split(" ")[0][1:]
                    
                    tbl_sign = temp.split("}")[1][:-1]

                    columns = temp.split("{")[1].split("}")[0]
                    columns = columns.split(",")
                    print(columns)
                    
                    columns_dict = dict()
                    
                    for column in columns:
                        column = column.split(" ")
                        columns_dict[column[1]] = column[0]

                    tbl_list.append( (tbl_name , tbl_sign , columns_dict) )
                    
                else:
                    pass

                temp = dbfile.readlines(1)

        self.TableList = tbl_list
        return tbl_list


    def ReadData(self, table_name, pattern_dict, limit=0):
        data_list = list()
        tbl_sign = None
        for table in self.TableList:
            if table[0]==table_name:
                tbl_sign = table[1]

        if not(tbl_sign):
            return False
        
        with open(self.CurrentDB , "r") as dbfile:
            temp = dbfile.readlines(1)
            while len(temp)!=0:
                temp = temp[0]
                if temp[:10]==tbl_sign:
                    temp = temp.replace("\n","")
                    temp = temp.split(":")[1]
                    temp = temp.split(",")
                    if self._match_with_pattern(temp,pattern_dict):
                        data_list.append(temp)

                temp = dbfile.readlines(1)

        return data_list



    def _match_with_pattern(self, data, pattern):
        return True




    
