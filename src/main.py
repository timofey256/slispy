import sys
import Parser, Eval

def run(program : str):
    t = Parser.Tokenizer()
    p = Parser.Parser()
    tokens = t.tokenize(program)
    ast = p.parse(tokens)
    return Eval.eval(ast)

if __name__ == "__main__":
    path = sys.argv[1][6:]
    f = open(path, "r")
    program = "(" + f.read() + ")" 
    print(run(program))
