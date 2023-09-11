import Types
from Environment import Environment

global_env = Environment()  # Global scope

"""
Main function which evaluates value of expression.
"""
def eval(exp : Types.Exp, e = global_env):
    if isinstance(exp, Types.Symbol):   
        return e.get_var(exp)
    elif isinstance(exp, Types.Number):    
        return exp            
    
    op = exp[0]
    args = exp[1:]
    if op == 'quote': 
        return args[0]
    elif op == "if":
        (_, test, conseq, alt) = exp
        exp = (conseq if eval(test, e) else alt)
        return eval(exp, e)
    elif op == "define":           
        (_, symbol, exp) = exp
        e.set_var(symbol, eval(exp, e))
        return None
    elif op == "set!":
        (symbol, value) = args
        e.set_var(symbol, eval(value, e))
        return None
    elif op == "lambda":
        (parms, body) = args
        return Procedure(parms, body, e)

    proc = eval(op, e)
    evaluated_args = []
    for arg in args:
        evaluated_arg = eval(arg, e)
        e.register_evaluated_arg(evaluated_arg)
        evaluated_args.append(evaluated_arg)
    
    # if 'proc', in fact, is not a function. might be, for example, a sequence of statements:
    if not callable(proc):
        for arg in evaluated_args[::-1]:
            if arg is not None:
                return arg
        return proc
    # 'proc' is a function:
    else:
        return proc(*evaluated_args)

"""
The Procedure class implements function with arguments.
"""
# (To be honest, it would be better to put this class into Types.py
# but i couldn't solve a problem with two-way importing: here, it Eval.py we use the Procedure class
# and in the class we also use eval() function)
class Procedure:
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        function_env = Environment(self.parms, args, self.env)
        return eval(self.body, function_env)
