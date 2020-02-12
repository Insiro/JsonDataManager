import os
import json
from enum import Enum
from typing import Any, Union, List
from DataNode import DataNode


class direction(Enum):
    LEFT = True
    RIGHT = False


class Collection:
    __dirname: str = ""
    __collectionName: Union[str, None] = None
    __root: Any = None

    def __init__(self, collectionName, baseRoot: str, generate=False):
        dirname = os.path.join(baseRoot, collectionName)
        self.__dirname = dirname
        if generate:
            try:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                    self.__collectionName = collectionName
                else:
                    print("Error : Already Exists collection")
            except OSError:
                print("Error : Creating collection. " + collectionName)
        else:
            if os.path.exists(dirname):
                self.__collectionName = collectionName
                self.__load()
            else:
                print("Error : Not Exists collection")

    def __str__(self):
        return self.__collectionName

    def __load(self):
        filelist = os.listdir(self.__dirname)
        for file in filelist:
            if file[-5:] == ".json":
                with open(os.path.join(self.__dirname, file), "r") as jsonfile:
                    data = json.load(jsonfile)
                    self.insert(data, file[:-5])

    def __rotate(self, direction: direction, rotateRoot: DataNode) -> bool:
        parent = rotateRoot.parent
        if direction == direction.LEFT:
            right = rotateRoot.right
            if right == None:
                return False
            rotateRoot.right = right.left
            right.left = rotateRoot
            if rotateRoot == self.__root:
                self.__root == right
            elif parent.left == rotateRoot:
                parent.left = right
            else:
                parent.right = right
            rotateRoot.updateNodeCount()
            right.updateNodeCount()
        else:
            left = rotateRoot.left
            if left == None:
                return False
            rotateRoot.left = left.right
            left.right = rotateRoot
            if rotateRoot == self.__root:
                self.__root == left
            elif parent.left == rotateRoot:
                parent.left = left
            else:
                parent.right = left
            rotateRoot.updateNodeCount()
            left.updateNodeCount()
        return True

    def __rebalance(self, root: DataNode):
        while root != None:
            balance = root.getBalance()
            if balance > 1:
                sub = root.left
                if balance < sub.getBalance():
                    self.__rotate(direction.LEFT, sub)
                self.__rotate(direction.RIGHT, root)
            elif balance < -1:
                sub = root.right
                if balance > sub.getBalance():
                    self.__rotate(direction.RIGHT, sub)
                self.__rotate(direction.LEFT, root)
            self.updateHeight(sub)
            root = root.parent

    def updateHeight(self, node: DataNode):
        while node != None:
            node.updateHeight()
            node = node.parent

    def insert(self, data: dict, dataID: str) -> Union[DataNode, None]:
        if self.__collectionName == None:
            print("Error : NULL collection")
            return None
        node = DataNode(data, dataID, self.__dirname)
        if self.__root == None:
            self.__root = node
            return node
        instance = self.__root
        while True:
            if instance.__str__() == dataID and instance.__str__() != None:
                print("exests Node")
                return None
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
        instance = node.parent
        while instance != None:
            instance.updateNodeCount()
            instance = instance.parent
        self.__rebalance(node.parent.parent)
        return node

    def delete(self, data: Union[str, DataNode, None]) -> str:
        if self.__collectionName == None:
            print("Error : NULL collection")
            return "Error : Null collection"
        elif data == None:
            return "Error : Null Data"
        dataID: str = str(data)
        try:
            os.remove("/" + self.__dirname + "/" + dataID + ".json")
        except OSError:
            return "Error : remove File : " + dataID
        if not isinstance(data, DataNode):
            data = self.getNode(dataID)
        while data.left != None and data.right != None:
            if data.left != None:
                self.__rotate(direction.RIGHT, data)
            elif data.right != None:
                self.__rotate(direction.LEFT, data)
        parent = data.parent
        if self.__root == data:
            self.__root = None
        elif parent.left == data:
            parent.left = None
        else:
            parent.right = None
        del data
        self.__rebalance(parent.parent)
        return "success"

    def getRoot(self) -> Union[DataNode, None]:
        return self.__root

    def getNode(self, dataID: str) -> Union[DataNode, None]:
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
    def getAllNode(self) -> List[DataNode]:
        stack = []
        result: List[DataNode] = list()
        instance: DataNode = self.__root
        stack.append([instance, None])
        return result

    def drop(self):
        if self.__collectionName == None:
            print("Error : NULL collection")
            return
        self.__collectionName = None
        self.__root = None
        fail_list = list()
        for node in self.getAllNode():
            r = self.delete(node)
            if r != None:
                fail_list.append(r)
        if len(fail_list) == 0:
            try:
                os.rmdir(self.__dirname)
                return
            except:
                print("Error failed to remove folder ", self.__dirname)
        print("Error failed to remove folder ", self.__dirname)
