import os
import json
from typing import Any, Union
from .DataNode import DataNode


class database:
    __dirname: str = ""
    __dbName: Union[str, None] = None
    __root: Any = None
    __tail: Any = None

    def __init__(self, dbName, baseRoot: str, generate=False):
        dirname = os.path.join(baseRoot, dbName)
        self.__dirname = dirname
        if generate:
            try:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                    self.__dbName = dbName
                else:
                    print("Error : Already Exists DB")
            except OSError:
                print("Error : Creating DB. " + dbName)
        else:
            if os.path.exists(dirname):
                self.__dbName = dbName
                self.__load()
            else:
                print("Error : Not Exists DB")

    def __str__(self):
        return self.__dbName

    def __load(self):
        filelist = os.listdir(self.__dirname)
        for file in filelist:
            if file[-5:] == ".json":
                with open(self.__dirname + "/" + file, "r") as jsonfile:
                    data = json.load(jsonfile)
                    self.insert(data, file[:-5], False)

    def insert(self, data: dict, dataID: str, savefile=True):
        if self.__dbName == None:
            print("Error : NULL DB")
            return "Error : NULL DB"
        node = DataNode(data, dataID, self.__dirname)
        if self.__root == None:
            self.__root = node
            self.__tail = node
            if savefile:
                self.__root.commit()
            return
        instance = self.__root
        while True:
            if instance.__str__() == dataID and instance.__str__() != None:
                print("exests Node")
                return "exests Node"
            elif instance.__str__() > dataID:
                if instance.left == None:
                    instance.left = node
                    node.parent = instance
                    if self.__tail == instance:
                        self.tail = node
                    if savefile:
                        node.commit()
                    break
                else:
                    instance = instance.left
            else:
                if instance.right == None:
                    instance.right = node
                    node.parent = instance
                    if instance == self.__tail or instance.left == self.__tail:
                        self.__tail = node
                    if savefile:
                        node.commit()
                    break
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
            os.remove("/" + self.__dirname + "/" + dataID + ".json")
        except OSError:
            print("Error : delete Data on fileSystem", self.__dbName, dataID)

    def rebalance(self):
        # TODO:rebalce
        pass

    def getHead(self):
        return self.__root

    def getTail(self):
        return self.__tail

    def drop(self):
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        self.__dbName = None
        self.__root = None
        # TODO:delete all files
        pass
