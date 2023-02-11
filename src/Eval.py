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
    if op is "if":               
        (syntax_if, test, conseq, alt) = exp
        exp = (conseq if eval(test, e) else alt)
        return eval(exp, e.env)
    elif op is "define":           
        (_, symbol, exp) = exp
        e.env[symbol] = eval(exp, e)
    elif op is "set!":
        (symbol, value) = args
        e.env[symbol] = eval(value, e)
    elif op is "lambda":
        (parms, body) = args
        return Types.Procedure(parms, body, e)
    else:                          
        proc = eval(op, e)
        args = [eval(arg, e) for arg in args]
        return proc(*args)