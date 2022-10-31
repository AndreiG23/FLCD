from collections import deque


class HashTable:

    def __init__(self, size) -> None:
        self.__size = size        
        self.__nrElements = 0     
        self.__elements = [deque() for _ in range(size)]
    
    def hash(self, key):
        key = str(key)
        return (self.val(key) % self.__size)

    def val(self, stringKey):
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

    def size(self):
        return self.__nrElements


