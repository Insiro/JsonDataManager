from typing import Any, Union, List
import datetime
import os
import json


class DataNode:
    __fileName: str
    __dirName: str
    __data: dict
    parent: Any
    left: Any
    right: Any
    __height: int
    __balance: int

    def __init__(self, data: dict, dataID: str, dirName: str):
        self.__data = data
        self.__dirName = dirName
        self.__fileName = dataID
        self.__height = 1
        self.__balance = 0
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self):
        return self.__fileName

    def setData(self, data: dict):
        self.__data = data

    def getData(self) -> dict:
        return json.dumps(self.__data, indent="\t", ensure_ascii=False)

    def updateData(self, data: dict):
        self.__data.update(data)

    def updateOne(self, key: str, data: Union[str, dict]):
        if type(data) == str:
            if data[0] == "{" and data[-1] == "}":
                data = json.loads(data.replace('\\"', '"'))
            elif data[0] == "[" and data[-1] == "]":
                data = '{ "data" : ' + data.replace('\\"', '"') + "}"
                data = data["data"]
        self.__data[key] = data

    def commit(self) -> bool:
        self.__data["time"] = str(datetime.datetime.now())
        file: str = os.path.join(self.__dirName, self.__fileName + ".json")
        try:
            with open(file, "w", encoding="UTF8") as jsonfile:
                json.dump(self.__data, jsonfile, indent="\t", ensure_ascii=False)
        except:
            return False
        return True

    def getInfo(self) -> str:
        return (
            "nodeName : "
            + self.__fileName
            + "\nparent : "
            + self.parent.__str__()
            + "\nleft : "
            + self.left.__str__()
            + "\tright : "
            + self.right.__str__()
        )

    def load(self) -> bool:
        file: str = os.path.join(self.__dirName, self.__fileName)
        if os.path.isfile(file):
            with open(file) as jsonfile:
                self.data = json.load(jsonfile)
            return True
        return False

    def getHeight(self):
        return self.__height

    def getBalance(self):
        return self.__balance

    def updateHeight(self):
        lh = self.left.getHeight() if self.left != None else 0
        rh = self.right.getHeight() if self.right != None else 0
        self.__height = max(lh, rh) + 1
        self.__balance = lh - rh

