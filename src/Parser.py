import Types

class Parser:
    def __init__(self) -> None:
        pass
        
    def parse(self, tokens: list) -> Types.Exp:
        stack = []
        expr = []
        
        for token in tokens:
            if token == '(':
                stack.append(expr)
                expr = []
            elif token == ')':
                if not stack:
                    raise SyntaxError('Unexpected syntax.')
                nested_expr = expr
                expr = stack.pop()
                expr.append(nested_expr)
            else:
                expr.append(Atom(token).value)
        
        if stack:
            raise SyntaxError('Unexpected EOF.')
        
        return expr[0]
        
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
