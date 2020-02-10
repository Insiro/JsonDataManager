from typing import Any, Union
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

    def __init__(self, data: dict, dataID: str, dirName: str):
        self.__data = data
        self.__dirName = dirName
        self.__fileName = dataID
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self):
        return self.__str__()

    def set_data(self, data: dict):
        self.__data = data

    def get_data(self) -> dict:
        return self.__data

    def commit(self) -> bool:
        self.data["time"] = str(datetime.datetime.now())
        file: str = os.path.join(self.__dirName, self.__fileName + ".json")
        try:
            with open(file, "w") as jsonfile:
                json.dump(self.__data, jsonfile, indent="\t")
        except:
            return False
        return True

    def load(self) -> bool:
        file: str = os.path.join(self.__dirName, self.__fileName)
        if os.path.isfile(file):
            with open(file) as jsonfile:
                self.data = json.load(jsonfile)
            return True
        return False
