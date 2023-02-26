"""
Memory was implemented using dicitionary.
"""

import math
import operator as op
import Types
import StandardLibrary as stl

class Environment:
    """
    parms, args are used to add new variables in some scope
    outer is an outer scope 
    """
    def __init__(self, parms=(), args=(), outer = None):
        self.env = {}
        if outer is not None:
            self.env = outer.env
        else:
            self.__set_default_env()
        self.env.update(zip(parms, args))
        self.outer = outer


    def find(self, key):
        if key in self.env:
            return self.env[key]
        # If we can not find a variable in current scope,
        # then try it in outer scope ("in more global scope" so to say) 
        elif self.outer is not None:
            return self.outer.find(key)
        return None
    
    def update(self, parms=(), args=()):
        self.env.update(zip(parms, args))

    """
    Sets default functions and variables in the language.
    """
    def __set_default_env(self):
        self.env.update(vars(math))
        self.env.update({
            '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
            '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
            'abs':     abs,
            'append':  op.add,  
            'apply':   lambda proc, args: proc(*args),
            'begin':   lambda *x: x[-1],
            'car':     lambda x: x[0],
            'cdr':     lambda x: x[1:], 
            'setcar':  stl.setcar,
            'setcdr':  stl.setcdr,
            'cons':    lambda x,y: [x] + y,
            'eq?':     op.is_, 
            'expt':    pow,
            'equal?':  op.eq, 
            'length':  len, 
            'list':    lambda *x: Types.List(x), 
            'list?':   lambda x: isinstance(x, Types.List), 
            'map':     map,
            'max':     max,
            'min':     min,
            'not':     op.not_,
            'null?':   lambda x: x == [], 
            'number?': lambda x: isinstance(x, Types.Number),  
            'print':   print,
            'procedure?': callable,
            'round':   round,
            'symbol?': lambda x: isinstance(x, Types.Symbol),
            })
