import Types

class Parser:
    def __init__(self) -> None:
        pass

    def parse(self, tokens : list) -> Types.Exp:
        if len(tokens) == 0:
            raise SyntaxError('Unexpected EOF.')
        
        token = tokens.pop(0)

        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(self.parse(tokens))
            tokens.pop(0) # pop off ')'
            return L
        
        elif token == ')':
            raise SyntaxError('Unexpected syntax.')
        
        else:
            atom = Atom(token)
            return atom.value
        
"""
The Tokenizer class divides source file into so-called tokens (= elements which we structure
to create AST of a program)
"""
class Tokenizer:
    def tokenize(self, program : str) -> list:
        return program.replace('(', ' ( ').replace(')', ' ) ').split()

"""
Atom is the most smallest object in Lisp which we can not
eval further.
"""
class Atom:
    def __init__(self, value) -> None:
        self.value = self.__set__value(value)
    
    def __set__value(self, value):
        try: return int(value)
        except ValueError:
            try: return float(value)
            except ValueError:
                return Types.Symbol(value)