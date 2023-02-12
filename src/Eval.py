import Types
from Environment import Environment

global_env = Environment()

def eval(exp : Types.Exp, e = global_env):
    if isinstance(exp, Types.Symbol):   
        return e.env[exp]
    elif isinstance(exp, Types.Number):    
        return exp            
    
    op = exp[0]
    args = exp[1:]
    if op == 'quote':            # quotation
        return args[0]
    elif op == "if":               
        (syntax_if, test, conseq, alt) = exp
        exp = (conseq if eval(test, e) else alt)
        return eval(exp, e)
    elif op == "define":           
        (_, symbol, exp) = exp
        e.env[symbol] = eval(exp, e)
    elif op == "set!":
        (symbol, value) = args
        e.env[symbol] = eval(value, e)
    elif op == "lambda":
        (parms, body) = args
        return Procedure(parms, body, e)
    else:           
        proc = eval(op, e)
        args = [eval(arg, e) for arg in args]
        if proc is None and args is not None:
            for arg in args:
                if arg is not None:
                    return arg
        return proc(*args)

class Procedure:
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        function_env = Environment(self.parms, args, self.env)
        return eval(self.body, function_env)