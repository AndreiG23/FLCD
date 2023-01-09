from Grammar import Grammar

class UI:
    def __init__(self) -> None:
        self.grammar = Grammar()
        self.parser = None
        self.cmds = {
            '1': self.printGrammar,
            '2': self.checkCFG,
        }

    def grammarMenu(self):
        print("\n1. Print grammar")
        print("2. Check CFG")
        print("x: back")

    def run(self):
            while True:
                grammarFile = input("\nGrammar file: ")
                if grammarFile == 'x':
                    return
                self.chooseGrammar(grammarFile)
                self.grammarRun()
    
    def grammarRun(self):
        self.grammarMenu()
        while True:
            cmd = input(" > ")
            if cmd == 'x':
                return
            if cmd == 'm':
                self.grammarMenu()
            if cmd in self.cmds:
                print("----------------------------------------------------")
                self.cmds[cmd]()
                print("----------------------------------------------------")
            else:
                print("no")
                continue

    def printGrammar(self):
        print("\n   Terminals: ")
        print(self.grammar.terminals)
        print("\n   Nonterminals: ")
        print(self.grammar.nonterminals)
        print("\n   Start symbol: ", self.grammar.start_symbol)
        print("\n   Productions: ")
        for prod in self.grammar.getProduction().keys():
            print(str(prod[0]) + " -> " + str(self.grammar.getProduction()[prod]))

    def checkCFG(self):
        print(self.grammar.isCFG())

    def chooseGrammar(self, file_path):
        self.grammar.read_from_file(file_path)
        