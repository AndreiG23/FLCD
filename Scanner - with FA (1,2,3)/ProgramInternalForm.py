class PIF:
    def __init__(self) -> None:
        self.__content = []

    def add(self, token, index):
        self.__content.append((token, index))

    def __str__(self) -> str:
        result = ""
        for pair in self.__content:
            result += "{:<12} ->   {:<15}\n".format(pair[0],str(pair[1]))
        if result == "":
            return "{}"
        return result
