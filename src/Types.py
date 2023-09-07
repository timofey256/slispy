"""
Types which are used in this Lisp-like language implementation.
"""

class ConsCell:
    def __init__(self, args):
        if len(args) > 2: raise Exception("Too many arguments for cons")
        self.car = args[0]
        self.cdr = args[1]

    def to_list(self):
        l = [self.car]
        if (isinstance(self.cdr, ConsCell)):
            return l + self.cdr.to_list()
        else: 
            return l 

Symbol = str
Cons = ConsCell 
Number = (int, float)
Atom = (Symbol, Number)
Exp = (Atom, Cons)