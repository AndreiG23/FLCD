

from HashTable import HashTable


class SymbolTable:

    def __init__(self, size) -> None:
        self.__ht = HashTable(size)


    def add(self, key):
        return self.__ht.add(key)

    def getPosition(self, key):
        return self.__ht.getPosition(key)

    def exists(self, key):
        return self.__ht.getPosition(key)

    def __str__(self):
        return str(self.__ht)

    def size(self):
        return self.__ht.size()
