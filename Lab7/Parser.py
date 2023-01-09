from collections import deque
from typing import Tuple, List


from Grammar import Grammar


class RecursiveDescendantParser:
    def __init__(self, grammar: Grammar, out_file):
        self._grammar = grammar
        self.output_file = out_file
        self.init_output_file()

    def read_sequence(self, sequence_file)->Tuple:
            sequence = ()
            with open(sequence_file) as file:
                if sequence_file == "PIF.out":
                    line = file.readline()
                    line = file.readline()
                    while line:
                        elems_line = line.split(" ")
                        sequence = sequence + tuple(str(elems_line[0]))
                        line = file.readline()
                else:
                    line = file.readline()
                    while line:
                        sequence = sequence + tuple(str(line[0:-1]))
                        line = file.readline()
            print(sequence)
            return sequence
    
    def init_output_file(self): #creates the given file
        file = open(self.output_file, 'w')
        file.write("")
        file.close()

    def write_in_output_file(self, message):
        with open(self.output_file, 'a') as file:
            file.write(message + "\n")


    def parse(self, word: Tuple):
        config = RecursiveDescendantConfiguration(self._grammar)
        while config.s not in {'f', 'e'}:
            if config.s == 'q':
                if config.i == len(word) and len(config.inputStack) == 0:
                    config.success()
                else:
                    if len(config.inputStack) > 0 and config.inputStack[-1] in self._grammar.N:
                        config.expand()
                    else:
                        if config.i < len(word) and len(config.inputStack) > 0 and config.inputStack[-1] == word[config.i]:
                            config.advance()
                        else:
                            config.momentaryInsuccess()
            else:
                if config.s == 'b':
                    if len(config.workingStack) > 0 and config.workingStack[-1] in self._grammar.Sigma:
                        config.back()
                    elif len(config.workingStack) > 0:
                        config.anotherTry()

        if config.s == 'e':
            print('Error at line ' + str(config.lastIndex + 1))
            self.write_in_output_file('Error at line ' + str(config.lastIndex + 1))
            return ParserOutput(self._grammar, [])
        print('Sequence accepted')
        self.write_in_output_file('Sequence accepted')
        self.write_in_output_file(str(ParserOutput._getTree(self._grammar,config.workingStack)))

class ParserOutput:
    def __init__(self, grammar, productionString):
        self.tree = self._getTree(grammar, productionString)
        self.grammar = grammar
        self.productionString = productionString

    @staticmethod
    def _getTree(grammar, productionString):
        
        print(productionString)
        return productionString

class RecursiveDescendantConfiguration:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self.s = 'q'
        self.i = 0
        self.lastIndex = 0
        self.workingStack: List[str] = []
        self.inputStack: List[str] = [grammar.S]

    def expand(self):
        currentSymbol = self.inputStack.pop()
        production = self._grammar.getProds((currentSymbol, ))
        if production[0] != ('eps', ):
            self.inputStack += reversed(production[0])
        self.workingStack.append(currentSymbol + "$0")

    def advance(self):
        self.i += 1
        terminal = self.inputStack.pop()
        self.workingStack.append(terminal)

    def momentaryInsuccess(self):
        self.s = 'b'

    def back(self):
        if self.i > self.lastIndex :
            self.lastIndex = self.i
        self.i -= 1
        terminal = self.workingStack.pop()
        self.inputStack.append(terminal)

    def anotherTry(self):
        annotatedSymbol = self.workingStack.pop()
        nonterminal, productionNumber = annotatedSymbol.split("$")
        productionNumber = int(productionNumber)
        productions = self._grammar.getProds((nonterminal, ))

        currentProduction = productions[productionNumber]
        for prod in currentProduction:
            if prod != "eps":
                _ = self.inputStack.pop()

        if productionNumber < len(productions) - 1:
            newProd = productions[productionNumber + 1]
            if newProd != ('eps', ):
                self.inputStack += reversed(newProd)
            self.workingStack.append(nonterminal + "${0}".format(productionNumber + 1))
            self.s = 'q'
            return

        if self.i == 0 and nonterminal == self._grammar.S:
            self.s = 'e'
            return

        self.inputStack.append(nonterminal)

    def success(self):
        self.s = 'f'