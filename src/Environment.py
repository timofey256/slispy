import math
import operator as op
import Types
import StandardLibrary as stl
import sys
from VirtualMemory import VM_Manager

class Environment:
    """
    parms, args are used to add new variables in some scope
    outer is an outer scope 
    """
    def __init__(self, parms=(), args=(), outer = None):
        self.__env = {}
        if outer is None:
            self.__set_default_env()
        self.update(dict(zip(parms, args)))
        self.outer = outer
        print(self.outer)

    def set_var(self, key, value):
        vm = VM_Manager.get_instance()

        if key in self.__env:
            block = vm.heap[self.__env[key]]
            block.data = value
        else:
            (new_block, index) = vm.malloc(sys.getsizeof(value))
            if new_block is None:
                raise Exception("Not enough memory.")
            
            new_block.data = value
            self.__env[key] = index

    def get_var(self, key):
        vm = VM_Manager.get_instance()
        value = self._find(key)

        if value is None:
            raise Exception(f"{key} wasn't defined")
        else:
            return value        
    
    def get_env(self):
        return self.__env

    def update(self, v):
        for item in v.items():
            self.set_var(item[0], item[1])

    def _find(self, key):
        vm = VM_Manager.get_instance()
        if key in self.__env:
            print("exists")
            index = self.__env[key]
            block = vm.heap[index]
            return block.data
        # If we can not find a variable in current scope,
        # then try it in outer scope ("in more global scope" so to say) 
        elif self.outer is not None:
            return self.outer._find(key)
        return None
    
    """
    Sets default functions and variables in the language.
    """
    def __set_default_env(self):
        self.update(vars(math))
        self.update({
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