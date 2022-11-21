class FiniteAutomata:

    def __init__(self) -> None:
        self.states = []
        self.alphabet = []
        self.initial = None
        self.finals = []
        self.transitions = {}


    def read_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = [line.replace('\n', "").strip() for line in lines]

            self.states = lines[0].split(" ")
            self.alphabet = lines[1].split(" ")
            self.initial = lines[2]
            self.finals = lines[3].split(" ")
            for index in range(4, len(lines)):
                # read a transition
                trans = lines[index].split(" ")
                initial = trans[0]
                route = trans[1]
                final = trans[2]

                if (initial, route) in self.transitions.keys():
                    self.transitions[(initial, route)].append(final)
                else:
                    self.transitions[(initial, route)] = [final]

        return self.validate()

    def validate(self):
        # validate initial state
        if self.initial not in self.states:
            return (False, "The initial state must be among the states")
        # validate final states
        for final in self.finals:
            if final not in self.states:
                return (False, "All final states must be among the states")
        
        #validate transitions
        for tr in self.transitions.keys():
            if tr[0] not in self.states or tr[1] not in self.alphabet:
                return (False, "Transitions must be in the form (state, alphabet element, state)")
            for finalState in self.transitions[tr]:
                if finalState not in self.states:
                    return (False, "Transitions must be in the form (state, alphabet element, state)")

        # states and alphabet don't intersect
        for state in self.states:
            if state in self.alphabet:
                return (False, "States and alphabet must not overlap")
        
        return (True, "")


    def isDFA(self):
        for key in self.transitions.keys():
            if len(self.transitions[key]) > 1:
                return False
        return True

    def isSequenceAccepted(self, sequence):
        if not self.isDFA():
            return False
        state = self.initial
        for symbol in sequence:
            if (state, symbol) in self.transitions.keys():
                state = self.transitions[(state, symbol)][0]
            else:
                return False
        return state in self.finals        

    def getStates(self):
        return self.states
    def getAlphabet(self):
        return self.alphabet
    def getInitial(self):
        return self.initial
    def getFinalStates(self):
        return self.finals
    def getTransitions(self):
        return self.transitions
