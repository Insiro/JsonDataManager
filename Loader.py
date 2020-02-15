import sys, os
from typing import Union, List

import json

from Collection import Collection
from DataNode import DataNode


class Loader:
    __newDataRoot: str
    __dataRoot: List[str]
    __collections: List[Collection]

    def __init__(self, runserver=False):
        with open("JDMconfig.json") as config:
            configlist = json.load(config)
            self.__newDataRoot = configlist["newDataRoot"]
            self.__dataRoot = configlist["dataRoot"]
            self.__collections = list()

    def getCollectionList(self) -> List[str]:
        r = list()
        for i in self.__collections:
            r.append(i.__str__())
        return r

    def loadCollection(self, collectionName: str):
        if collectionName == "":
            print("fail")
            return
        elif collectionName == "*":
            for item in os.listdir(self.__newDataRoot):
                dirname = os.path.join(self.__newDataRoot, item)
                if os.path.isdir(dirname):
                    self.__collections.append(
                        Collection(
                            baseRoot=self.__newDataRoot,
                            collectionName=item,
                            generate=False,
                        )
                    )
            for path in self.__dataRoot:
                for item in os.listdir(path):
                    collectionPath = os.path.join(path, item)
                    if os.path.isdir(collectionPath):
                        self.__collections.append(
                            Collection(
                                baseRoot=path, collectionName=item, generate=False,
                            )
                        )
            return
        collectionPath: str = os.path.join(self.__newDataRoot, collectionName)
        if os.path.isdir(collectionPath):
            self.__collections.append(
                Collection(
                    baseRoot=self.__newDataRoot,
                    collectionName=collectionName,
                    generate=False,
                )
            )
            return
        for path in self.__dataRoot:
            collectionPath = os.path.join(path, collectionName)
            if os.path.isdir(collectionPath):
                self.__collections.append(
                    Collection(
                        baseRoot=path, collectionName=collectionName, generate=False
                    )
                )
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
                print(self.getCollectionList())
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
            elif command == "setdata":
                if node == None:
                    print("NULL Node")
                    continue
                elif option == "":
                    option = input("insert your json file Path or 0: ")
                if option == 0 or option == "":
                    continue
                elif os.path.isfile(option):
                    with open(option, "r", encoding="UTF-8") as jfile:
                        node.setData(json.load(jfile))
                        continue
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

