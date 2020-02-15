import sys, os
from typing import Union, List

import json

from Collection import Collection


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

    def __CollectionExcute(self, collection):
        if collection == None:
            print("Null collection")
            return
        while True:
            exe = input(collection.__str__() + "> ").strip().split(" ")
            command = exe[0].lower()
            if command == "insert":
                while True:
                    print("dataID : ", exe[1], "input 0 for cancel")
                    path = input("dataID : ", exe[1], ", input json path : ")
                    if path == 0:
                        break
                    elif os.path.isfile(path):
                        with open(path, "r") as jfile:
                            collection.insert(exe[1], jfile)
                            break
            elif command == "delete":
                result = collection.delete(exe[1])
                print(result)
            elif command == "getnode":
                dataID: str
                if len(exe) == 1:
                    dataID = input("input Data ID : ")
                else:
                    dataID = exe[1]
                self.__nodeExcute(collection, collection.getNode(dataID))
            elif command == "drop":
                collection.drop()
            elif command == "list":
                print(collection.getNames())
            elif command == "exit":
                return
            elif command == "command":
                print("insert, delete, getNode, drop, list, exit")
            else:
                print("wrong command, for sea list type command")

    def __nodeExcute(self, collection, node):
        if node == None:
            print("Null node")
            return
        while True:
            exe = (
                input(collection.__str__() + ">" + node.__str__() + "> ")
                .strip()
                .split(" ")
            )
            command = exe[0].lower()
            if command == "exit":
                return
            elif command == "setdata":
                while True:
                    path = input("insert your json file Path or 0: ")
                    if path == 0:
                        break
                    elif os.path.isfile(path):
                        with open(path, "r") as jfile:
                            node.setData(json.load(jfile))
                            break
            elif command == "commit":
                node.commit()
            elif command == "getdata":
                print(node.getData())
            elif command == "load":
                print("success" if node.load() else "fail")
            elif command == "command":
                print("setData, commit, getData, load")
            else:
                print("wrong command, for sea list type command")

    def cui(self):
        while True:
            args = input(">").strip().split(" ")
            command = args[0].lower()
            if command == "command":
                print("exit, list, load, create, use, release")
            elif command == "exit":
                exit()
            elif command == "list":
                print(self.getCollectionList())
            elif command == "load":
                if len(args) < 2:
                    collectionName = input("input collection Name")
                else:
                    collectionName = args[1]
                self.loadCollection(collectionName)
                # load Collection
            elif command == "create":
                self.createCollection(args[1])
            elif command == "use":
                self.__CollectionExcute(self.getCollection(args[1]))
            elif command == "release":
                self.releaseCollection(args[1])
            else:
                print("wrong command, for sea list type command")

