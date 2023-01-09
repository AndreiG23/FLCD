class Grammar:
#recursive descendent
    def __init__(self) -> None:
        self.nonterminals = []
        self.terminals = []
        self.productions = {}
        self.start_symbol = None

    def read_from_file(self, file_path):
        self.nonterminals = []
        self.terminals = []
        self.productions = {}
        self.start_symbol = None

        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = [line.replace('\n', "").strip() for line in lines]

            self.nonterminals = lines[0].split(" ")

            self.terminals = lines[1].split(" ")

            self.start_symbol = lines[2]

            production_index = 0
            for index in range(3, len(lines)):
                
                production = lines[index]
                left, right = production.split('->')

                left = left.strip().split(' ')
                left = tuple(left)

                right = right.strip().split('|')
                for value in right:
                    production_index += 1
                    values = value.strip().split(' ')
                    if left in self.productions.keys():
                        self.productions[left].append((values, production_index))
                    else:
                        self.productions[left] = [(values, production_index)]

    
    def getTerminals(self):
        return self.terminals

    def getNonterminas(self):
        return self.nonterminals

    def getProduction(self):
        return self.productions

    def isCFG(self):
        for left in self.productions.keys():
            if len(left) != 1:
                return False
            if left[0] not in self.nonterminals:
                return False
        return True
           