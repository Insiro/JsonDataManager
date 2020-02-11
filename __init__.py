import sys
from typing import Union, List

import json
from dataController import *


class DB_Loader:
    __newDataRoot: str
    __DataRoot: List[str]
    __dbList: List[database]

    def __init__(self, runserver=False):
        with open("JDMconfig.json") as config:
            configlist = json.load(config)
            self.__newDataRoot = configlist["newDataRoot"]
            self.__DataRoot = configlist["dataRoot"]
            self.__dbList = list()

    def get_dbList(self) -> List[str]:
        r = list()
        for i in self.__dbList:
            r.append(i.__str__())
        return r

    def load_db(self, dbName: str):
        if dbName == "":
            return
        dbPath: str = os.path.join(self.__newDataRoot, dbName)
        if os.path.isdir(dbPath):
            self.__dbList.append(database(dbName, dbPath, False))
            return
        for path in self.__DataRoot:
            dbPath = os.path.join(path, dbName)
            if os.path.isdir(dbPath):
                self.__dbList.append(database(dbName, dbPath, False))
                return

    def reloase_DB(self, dbName: str):
        for db in self.__dbList:
            if db.__str__() == dbName:
                self.__dbList.remove(db)
                del db

    def create_db(self, dbName: str):
        if dbName == "":
            return
        self.__dbList.append(database(dbName, self.__newDataRoot, True))

    def get_db(self, dbName) -> Union[database, None]:
        for db in self.__dbList:
            if db.__str__() == dbName:
                return db
        return None

    def __dbExcute(self, db):
        if db == None:
            print("Null DB")
            return
        while True:
            exe = input(db, "> ").split(" ")
            if exe[0] == "insert":
                while True:
                    print("dataID : ", exe[1], "input 0 for cancel")
                    path = input("dataID : ", exe[1], ", input json path : ")
                    if path == 0:
                        break
                    elif os.path.isfile(path):
                        with open(path, "r") as jfile:
                            db.insert(exe[1], jfile)
                            break
            elif exe[0] == "delete":
                result = db.delete(exe[1])
                print(result)
            elif exe[0] == "get_node":
                self.__nodeExcute(db.get_node())
            elif exe[0] == "drop_db":
                db.drop()
            elif exe[0] == "exit":
                return
            else:
                "wrong instruct"

    def __nodeExcute(self, node):
        if node == None:
            print("Null node")
            return
        while True:
            exe = input(node, "> ").split(" ")
            if exe[0] == "exit":
                return
            elif exe[0] == "set_data":
                while True:
                    path = input("insert your json file Path or 0: ")
                    if path == 0:
                        break
                    elif os.path.isfile(path):
                        with open(path, "r") as jfile:
                            node.set_data(json.load(jfile))
                            break
            elif exe[0] == "commit":
                node.commit()
            elif exe[0] == "get_data":
                print(node.get_data())
            elif exe[0] == "load":
                print("success" if node.load() else "fail")
            else:
                print("wrong instruct")

    def cui(self):
        while True:
            cmi = input()
            args = cmi.split(" ")[0]
            if args[0] == "exit":
                exit()
            elif args[0] == "list":
                self.get_dbList()
            elif args[0] == "load":
                self.load_db(args[1])
                # load DataBase
            elif args[0] == "create":
                self.create_db(args[1])
            elif args[0] == "use":
                self.__dbExcute(self.get_db(args[1]))
            elif args[0] == "release":
                self.reloase_DB(args[1])
            else:
                print("Wrong args")


if __name__ == "__main__":
    arg = sys.argv[1:]
    if "server" in arg:
        roader = DB_Loader(runserver=True)
    else:
        roader = DB_Loader()
    roader.cui()
