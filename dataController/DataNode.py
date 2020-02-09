from typing import Any, Union
import datetime


class DataNode:
    __fileName: str
    __dirName: str
    __data: Union[dict, None]
    parent: Any
    left: Any
    right: Any

    def __init__(self, data: dict, dataID: str, dirName: str):
        self.__data = data
        self.__dirName = dirName
        self.__fileName = dataID
        self.parent = None
        self.left = None
        self.right = None

    def update(self, data: dict):
        __data = data

    def getData(self):
        if self.__data == None:
            with open("/" + self.__dirName + self.__fileName) as jsonfile:
                self.__data = json.load(jsonfile)
        return __data

    def __str__(self):
        return self.__fileName

    def commit(self):
        self.__data["time"] = str(datetime.datetime.now())
        with open(
            "./" + str(self.__dirName) + "/" + str(self.__fileName) + ".json", "w"
        ) as jsonfile:
            json.dump(self.__data, jsonfile, indent="\t")
