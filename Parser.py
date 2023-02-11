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

class Tokenizer:
    def __init__(self) -> None:
        pass

    def tokenize(self, program : str) -> list:
        return program.replace('(', ' ( ').replace(')', ' ) ').split()

class Atom:
    def __init__(self, value) -> None:
        self.value = self.__set__value(value)
    
    def __set__value(self, value):
        try: return int(value)
        except ValueError:
            try: return float(value)
            except ValueError:
                return Types.Symbol(value)