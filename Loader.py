import sys, os
from typing import Union, List

import json

from Collection import Collection
from DataNode import DataNode


class Loader:
    __newDataRoot: str
    __dataRoot: List[str]
    __collections: List[Collection]
    __colnamnes: List[str]

    def __init__(self, runserver=False):
        with open("JDMconfig.json") as config:
            configlist = json.load(config)
            self.__newDataRoot = configlist["newDataRoot"]
            self.__dataRoot = configlist["dataRoot"]
            self.__collections = list()
            self.__colnamnes = list()
            if self.__newDataRoot not in self.__dataRoot:
                self.__newDataRoot.insert(0, self.__newDataRoot)

    def loadCollection(self, collectionName: str):
        if collectionName == "" or collectionName == None:
            print("fail")
            return
        elif collectionName == "*":
            for path in self.__dataRoot:
                for item in os.listdir(path):
                    collectionPath = os.path.join(path, item)
                    if os.path.isdir(collectionPath) and item not in self.__colnamnes:
                        col = Collection(
                            baseRoot=path, collectionName=item, generate=False,
                        )
                        self.__collections.append(col)
                        self.__colnamnes.append(str(col))
            return
        elif collectionName in self.__colnamnes:
            print("duplicate Collection name")
            return
        collectionPath: str = os.path.join(self.__newDataRoot, collectionName)
        for path in self.__dataRoot:
            collectionPath = os.path.join(path, collectionName)
            if os.path.isdir(collectionPath):
                col = Collection(
                    baseRoot=path, collectionName=collectionName, generate=False
                )
                self.__collections.append(col)
                self.__colnamnes.append(col.__str__())
                return
        print("Error : Not Exists collection")

    def releaseCollection(self, collectionName: str):
        for collection in self.__collections:
            if collection.__str__() == collectionName:
                self.__collections.remove(collection)
                del collection

    def createCollection(self, collectionName: str):
        if collectionName == "":
            return
        self.__collections.append(Collection(collectionName, self.__newDataRoot, True))

    def getCollection(self, collectionName) -> Union[Collection, None]:
        for collection in self.__collections:
            if collection.__str__() == collectionName:
                return collection
        return None

    def cui(self):
        cole: Union[Collection] = None
        node: Union[DataNode] = None
        while True:
            output_string = (
                (str(cole) if cole != None else "")
                + " >"
                + (str(node) + " > " if node != None else " ")
            )
            args = input(output_string).strip().split(" ")
            option = " ".join(args[1:]).strip() if len(args) > 1 else ""
            command = args[0].lower()
            if command == "command":
                print(
                    "Global\t\t: exit, list, load, create, use, release"
                    + "\nCollection\t: insert, delete, getNode, drop, nodelist, exit"
                    + "\nNode\t\t: setData, commit, getData, load"
                )
            elif command == "exit":
                exit()
            elif command == "list":
                print(self.__colnamnes)
            elif command == "load":
                if option == "":
                    option = input("input collection Name").strip()
                if option == "" or option == "0":
                    continue
                self.loadCollection(option)
            elif command == "create":
                if option == "":
                    option = input("input collection names or 0").strip()
                if option == "" or option == "0":
                    continue
                self.createCollection(option)
            elif command == "use":
                cole = self.getCollection(option)
                node = None
            elif command == "release":
                if option == "" or option == "0":
                    option = input("input collection name or 0").strip()
                if option == "" or option == "0":
                    continue
                self.releaseCollection(option)
            # Collection part
            elif command == "insert":
                if cole == None:
                    print("NULL collection")
                    continue
                if option == "" or option == "0":
                    did = input("input dataID : ").strip()
                else:
                    did = option
                if did == "" or did == "0":
                    print("NULL dataID")
                    pass
                path = input("dataID : " + did + ", input json path or 0: ").strip()
                if path == 0 or path == "":
                    continue
                elif os.path.isfile(path):
                    with open(path, "r", encoding="UTF-8") as jfile:
                        cole.insert(did, jfile)
                        break
                else:
                    print("wrong path, cancel")
            elif command == "delete":
                if cole == None:
                    print("NULL collection")
                result = cole.delete(option)
                print(result)
                if option==node.__str__ ()):
                    self.node = None
            elif command == "getnode":
                if cole == None:
                    print("NULL collection")
                    continue
                if option == "":
                    option = input("input Data ID: ").strip()
                node = cole.getNode(option)
            elif command == "drop":
                if cole == None:
                    print("NULL collection")
                    continue
                cole.drop()
            elif command == "nodelist":
                if cole == None:
                    print("NULL collection")
                    continue
                print(cole.getNames())
            # Node part
            elif command == "update":
                if node == None:
                    print("NULL node")
                    continue
                print("input end for finish input")
                data = ""
                line = input("newDictData > ")
                while line.lower() != "end":
                    data += "\n" + line
                    line = input("newDictData > ")
                node.updateData(json.loads(data.replace('\\"', '"')))
            elif command == "setdata":
                if node == None:
                    print("NULL Node")
                    continue
                elif option == "":
                    option = input(
                        "data option\n1: json path\n2 : use console line\n3 : cancel\t> "
                    )
                if option == 0 or option == "":
                    continue
                elif option == "1":
                    if os.path.isfile(option):
                        path = input("json path")
                        with open(option, "r", encoding="UTF-8") as jfile:
                            node.setData(json.load(jfile))
                            continue
                elif option == "2":
                    print("input end for finish input")
                    data = ""
                    line = input("newDictData > ")
                    while line.lower() != "end":
                        data += "\n" + line
                        line = input("newDictData > ")
                    node.setData(json.loads(data.replace('\\"', '"')))
            elif command == "commit":
                if node == None:
                    print("NULL Node")
                    continue
                node.commit()
            elif command == "getdata":
                if node == None:
                    print("NULL Node")
                    continue
                print(node.getData())
            elif command == "load":
                if node == None:
                    print("NULL Node")
                    continue
                print("success" if node.load() else "fail")
            else:
                print("wrong command, for sea list type command")
