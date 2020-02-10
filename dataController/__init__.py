import os
import json
from typing import Any, Union, List
from .DataNode import DataNode
from enum import Enum


class __direction(Enum):
    LEFT = True
    RIGHT = False


class database:
    __dirname: str = ""
    __dbName: Union[str, None] = None
    __root: Any = None

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
                    self.insert(data, file[:-5])

    def __rotate(self, direction: __direction, rotateRoot: DataNode):
        parent = rotateRoot.parent
        if direction == __direction.LEFT:
            right = rotateRoot.right
            if right == None:
                print("error")
                return
            rotateRoot.right = right.left
            right.left = rotateRoot
            if rotateRoot == self.__root:
                self.__root == right
            elif parent.left == rotateRoot:
                parent.left = right
            else:
                parent.right = right
        else:
            left = rotateRoot.left
            if left == None:
                print("error")
                return
            rotateRoot.left = left.right
            left.right = rotateRoot
            if rotateRoot == self.__root:
                self.__root == left
            elif parent.left == rotateRoot:
                parent.left = left
            else:
                parent.right = left

    def __rebalance(self):
        # TODO:rebalce
        pass

    def insert(self, data: dict, dataID: str) -> DataNode:
        if self.__dbName == None:
            print("Error : NULL DB")
            return "Error : NULL DB"
        node = DataNode(data, dataID, self.__dirname)
        if self.__root == None:
            self.__root = node
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
                    break
                else:
                    instance = instance.left
            else:
                if instance.right == None:
                    instance.right = node
                    node.parent = instance
                    break
                else:
                    instance = instance.right
        self.__rebalance()
        return node

    def delete(self, data: Union(str, DataNode, None)) -> Union[str, None]:
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        elif data == None:
            return
        dataID: str = str(data)
        try:
            os.remove("/" + self.__dirname + "/" + dataID + ".json")
        except OSError:
            return dataID
        if not isinstance(data, DataNode):
            data = self.get_node(dataID)
        while data.left != None and data.right != None:
            if data.left != None:
                self.__rotate(__direction.RIGHT, data)
            elif data.right != None:
                self.__rotate(__direction.LEFT, data)
        parent = data.parent
        if self.__root == data:
            self.__root = None
        elif parent.left == data:
            parent.left = None
        else:
            parent.right = None
        del data
        self.__rebalance()
        return None

    def get_root(self) -> Union[DataNode, None]:
        return self.__root

    def get_node(self, dataID: str) -> Union[DataNode, None]:
        if self.__root == None:
            return None
        node: DataNode = self.__root
        while True:
            if node == None:
                return None
            elif node.__str__() == dataID:
                return node
            elif node.__str__() > dataID:
                node = node.left
            else:
                node = node.right
        return None

    # use dfs Search
    def get_allNode(self) -> List[DataNode]:
        stack = []
        result = list()
        instance: DataNode = self.__root
        stack.append([instance, None])
        return result

    def drop(self):
        if self.__dbName == None:
            print("Error : NULL DB")
            return
        self.__dbName = None
        self.__root = None
        fail_list = list()
        for node in self.get_allNode():
            r = self.delete(node)
            if r != None:
                fail_list.append(r)
        if len(fail_list) == 0:
            try:
                os.rmdir(self.__dirname)
            except:
                print("Error failed to remove folder ", self.__dirname)
        else:
            print("Error failed to remove folder ", self.__dirname)
        pass
