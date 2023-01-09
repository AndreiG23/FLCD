from Grammar import Grammar

from Parser import RecursiveDescendantParser,RecursiveDescendantConfiguration

myGrammar = Grammar.readFromFile("g1.txt")
parser = RecursiveDescendantParser(myGrammar, "out1.txt")
parser.parse(parser.read_sequence("seq.txt"))
#parser.parse(("b", "a", "c"))
#parser.parse(("a",))
#parser.parse(("b", "a"))
#parser.parse(("a", "c",))

