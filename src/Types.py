from Environment import Environment

Symbol = str
List = list
Number = (int, float)
Atom = (Symbol, Number)
Exp = (Atom, List)

class Procedure:
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return eval(self.body, Environment())