import os
import json
import datetime
from typing import Any, Union


class DataNode:
    __fileName: str
    __dbName: str
    __data: Union[dict, None]
    parent: Any
    left: Any
    right: Any

    def __init__(self, data: dict, dataID: str, dbName: str):
        self.__data = data
        self.__dbName = dbName
        self.__fileName = dataID
        self.parent = None
        self.left = None
        self.right = None

    def update(self, data: dict):
        __data = data

    def getData(self):
        if self.__data == None:
            self.__data = json.load("/" + self.__dbName + self.__fileName + ".json")
            pass
        return __data

    def __str__(self):
        return self.__fileName

    def commit(self):
        self.__data["time"] = datetime.datetime.now()
        json.dump(self.__data, "/" + self.__fileName + ".json", indent="\t")


class database:
    __dbName: Union[str, None] = None
    __root: Any
    __tail: Any

    def __init__(self, dbName, generate=False):
        if generate:
            try:
                if not os.path.exists(dbName):
                    os.makedirs(dbName)
                    self.__dbName = dbName
                else:
                    print("Error : Already Exists DB")
            except OSError:
                print("Error : Creating DB. " + dbName)
        else:
            if os.path.exists(dbName):
                self.__load()
            else:
                print("Error : Not Exists DB")

    def __str__(self):
        return self.__dbName

    def __load(self):
        filelist = os.listdir("/" + self.__dbName)
        for file in filelist:
            data = json.load("/" + self.__dbName + file)
            self.insert(data, file)

    def insert(self, data: dict, dataID: str):
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        elif self.__root == None:
            self.__root = DataNode(data, dataID, str(self.__dbName))
            self.__tail = self.__root
            return
        instance = self.__root
        while True:
            if instance.__str__() == dataID:
                print("exests Node")
                return
            elif instance.__str__() > dataID:
                if instance.left == None:
                    instance.left = DataNode(data, dataID, str(self.__dbName))
                    instance.left.parent = instance
                    if instance.right == None and self.__tail == instance:
                        self.tail = instance.left
                else:
                    instance = instance.left
            else:
                if instance.right == None:
                    instance.right.parent = instance
                    instance.right = DataNode(data, dataID, str(self.__dbName))
                    if instance == self.__tail or instance.left == self.__tail:
                        self.__tail = instance.right
                else:
                    instance = instance.right
        self.rebalance()

    def delete(self, dataID: str):
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        if self.__root:
            pass
        # TODO:remove Node

        try:
            self.rebalance()
            os.remove("/" + str(self.__dbName) + dataID + ".json")
        except OSError:
            print("Error : delete Data on fileSystem", self.__dbName, dataID)

    def rebalance(self):
        # TODO:rebalce
        pass

    def drop(self):
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        self.__dbName = None
        self.__root = None
        # TODO:delete all files
        pass
