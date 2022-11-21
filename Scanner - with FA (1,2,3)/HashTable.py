# 1b
# separate tables for identifiers, respectively constants (create 2 instances)
from collections import deque


class HashTable:

    def __init__(self, size) -> None:
        self.__size = size        # m=nr positions in hash table
        self.__nrElements = 0     # actual nr of ids/constants kept in table
        self.__elements = [deque() for _ in range(size)]
    
    def hash(self, key):
        key = str(key)
        return (self.val(key) % self.__size)

    def val(self, stringKey):
        # sum of ascii codes
        sum = 0
        for character in stringKey:
            sum += ord(character)
        return sum

    def add(self, key):
        if self.exists(key):
            return self.getPosition(key)
        self.__nrElements += 1
        hashValue = self.hash(key)
        self.__elements[hashValue].append(key)
        return self.getPosition(key)

    def getPosition(self, key):
        hashValue = self.hash(key)
        index = 0
        for element in self.__elements[hashValue]:
            if element == key:
                return (hashValue, index)
            index += 1
        return False

    def exists(self, key):
        if not self.getPosition(key):
            return False
        return True

    def __str__(self):
        string = ""
        for i in range(len(self.__elements)):
            if len(self.__elements[i]) == 0:
                continue

            stringlist = "{:<3} -> ".format(str(i))
            for el in self.__elements[i]:
                stringlist += "{:<10} | ".format(el)
            string += stringlist + "\n"
        
        if string == "":
            return "{}"
        return string

    def size(self):
        return self.__nrElements


