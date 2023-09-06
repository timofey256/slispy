"""
Types which are used in this Lisp-like language implementation.
"""

class ConsCell:
    def __init__(self, args):
        if len(args) > 2: raise Exception("Too many arguments for cons")
        print(f'\tConsCell args : {args}')
        self.car = args[0]
        self.cdr = args[1]

Symbol = str
Cons = ConsCell 
Number = (int, float)
Atom = (Symbol, Number)
Exp = (Atom, Cons)