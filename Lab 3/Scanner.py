import re
from utils import readTokens, readProgram
from SymbolTable import SymbolTable
from ProgramInternalForm import PIF

class Scanner:

    def __init__(self) -> None:
        self.operators, self.separators, self.keywords = readTokens("token.in")

        self.ST = SymbolTable(300)
        self.pif = PIF()

        self.errors = []


    def scan(self, file_path):
        program = readProgram(file_path)
        nrLine = 0

        for line in program:
            # we detect the tokens from the line
            nrLine +=1
            tokens = self.tokenize(line)

            for token in tokens:
                if self.isToken(token):
                    self.pif.add(token, (-1,-1))
                else:
                    if self.isIdentifier(token):
                        index = self.ST.add(token)
                        self.pif.add("id", index)
                    elif self.isConstant(token):
                        index = self.ST.add(token)
                        self.pif.add("const", index)
                    else:
                        self.error(token, nrLine)

        # handle errors
        if(len(self.errors) == 0):
            print("Lexically correct")
            self.generateOutput()
        else:
            print("Error")
            for err in self.errors:
                print(err)


    def error(self, token, nrLine):
        self.errors.append("Lexical error at line " + str(nrLine) + ": " + token)

    def generateOutput(self):
        with open("PIF.out", 'w') as file:
            file.write(str(self.pif))
        with open("ST.out", 'w') as file:
            file.write("Symbol Table implemented with Hash table\n\n")
            file.write(str(self.ST))
            file.write("\n\n")

    def tokenize(self, line):
        # remove spaces and newlines
        line = line.replace('\n', '').strip()
        if line == '':
            return []

        # handle the strings and the operators
        line, strings = self.search_for_strings(line)
        line = self.search_for_operators(line)

        # split the line by the separators
        for separator in self.separators:
            line = line.replace(separator, " "+separator+" ")
        tokens = line.split(" ")
        tokens = [t for t in tokens if t != '']

        # replace back the string tokens
        for i in range(len(tokens)):
            if re.match("^\$[0-9]+\$$", tokens[i]) is not None:
                tokens[i] = strings[int(tokens[i][1:-1])]

        return tokens


    def search_for_operators(self, line):
        result = ""
        i = 0
        while i < len(line):
            # check for compound operators
            if i+1<len(line) and self.isOperator(line[i]+line[i+1]):
                result += " " + line[i]+line[i+1] + " "
                i +=1
            # check for simple operators
            elif self.isOperator(line[i]):
                result += " " + line[i] + " "
            else:
                result += line[i]
            i +=1
        return result


    def search_for_strings(self, line):
        # replace the strings ("...") with $id$, where id is the index in the list of strings
        strings = []
        line_without_strings = ""

        i = 0
        isString = False
        string = ""

        while i<len(line):

            # when encountering a '"', its either the beginning or end of a string
            if line[i] == '"':
                # we add the finished string to the list as $index$
                if isString:
                    string += '\"'
                    strings.append(string)
                    line_without_strings += " $" + str(len(strings)-1) + "$ "
                # otherwise we start a new string
                else:
                    string = '\"'
                isString = not isString

            else:
                if isString:
                    string += line[i]
                else:
                    line_without_strings += line[i]
            i +=1

        if isString:
            strings.append(string)
            line_without_strings += " $" + str(len(strings)-1) + "$ "

        return line_without_strings, strings

    def isReservedWord(self, token):
        return token in self.keywords

    def isOperator(self, token):
        return token in self.operators

    def isSeparator(self, token):
        return token in self.separators

    def isToken(self, token):
        return self.isReservedWord(token) or self.isOperator(token) or self.isSeparator(token)

    def isIdentifier(self, token):
        return re.match("^[a-z][\w]*$", token) is not None

    def isConstant(self, token):
        return self.isNumber(token) or self.isString(token)

    def isNumber(self, token):
        return token == "0" or re.match("^-?[1-9][0-9]*$", token) is not None

    def isString(self, token):
        return re.match("^\"[A-Za-z0-9\.\?\!, ]*\"$", token) is not None

