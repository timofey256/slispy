import math
import operator as op
import sys
import random
import string

import Types
import StandardLibrary as stl
from VirtualMemory import VM_Manager

"""
Environment is used to represent current context during the execution time.

It stores pairs of variables in dictionary as <name : index in heap of VM>, 
can create new variables and return information about previously created ones.
"""
class Environment:
    """
    parms, args are used to add new variables in some scope
    outer is an outer scope 
    """
    def __init__(self, parms=(), args=(), outer = None):
        self.__env = {}
        self.outer = outer
        if outer is None:
            self.__set_default_env()
        self.__update(dict(zip(parms, args)))
        
        self.evaluated_args_num = 0 if outer==None else outer.evaluated_args_num

    def set_var(self, key, value):
        vm = VM_Manager.get_instance()

        index = self._find_env_var(key)
        #if index is not None:
        if self.__find_in_envs(key, self):
            block = vm.heap[index]
            block.data = value
            block.is_free = False
        else:
            (new_block, index) = self.__try_allocate_memory(vm, value)
            if new_block is None:
                raise Exception("Not enough memory.")
            
            new_block.data = value
            new_block.is_free = False
            self.__env[key] = index

    def register_evaluated_arg(self, value):
        self.evaluated_args_num += 1
        # adding also random prefix to prevent collisions with user's variables (user might declare e.g. "1", "evaluated_arg_1", etc.)
        random_prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        key = f'{random_prefix}_{self.evaluated_args_num}'
        self.set_var(key, value)

    def get_var(self, key):
        vm = VM_Manager.get_instance()
        value = self.__find(vm, key)

        if value is None:
            raise Exception(f"\"{key}\" wasn't defined")
        else:
            return value

    def get_env(self):
        return self.__env

    def force_gc(self):
        vm = VM_Manager.get_instance()
        vm.gc(self.__env)

    def __update(self, v):
        for item in v.items():
            self.set_var(item[0], item[1])

    def __try_allocate_memory(self, vm, data):
        new_block, index = None, None
        (new_block, index) = vm.malloc(sys.getsizeof(data))

        # If there's not enough memory, start garbage collector and then try to allocate again
        if new_block is None:
            vm.gc(self.__env)
            (new_block, index) = vm.malloc(sys.getsizeof(data))

        return (new_block, index)          
    
    def __find_in_envs(self, key, env):
        if env is None:
            return None
        
        if key in env.__env:
            return True
        else:
            return self.__find_in_envs(key, env.outer)
        
    def __find(self, vm, key):
        if key in self.__env:
            index = self.__env[key]
            block = vm.heap[index]
            return block.data
        # If we can not find a variable in current scope,
        # then try it in outer scope ("in more global scope" so to say) 
        elif self.outer is not None:
            return self.outer.__find(vm, key)
        return None

    def _find_env_var(self, key):
        if key in self.__env:
            return self.__env[key]
        elif self.outer is not None:
            return self.outer._find_env_var(key)
        return None
    
    """
    Sets default functions and variables in the language.
    """
    def __set_default_env(self):
        self.__update(vars(math))
        self.__update({
            '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
            '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
            'abs':     abs,
            'or':      lambda *x: stl.logical_or(*x),
            'and':     lambda *x: stl.logical_and(*x),
            'append':  op.add,  
            'apply':   lambda proc, args: proc(*args),
            'begin':   lambda *x: x[-1],
            'car':     lambda x: x.car,
            'cdr':     lambda x: x.cdr,
            'setcar':  stl.setcar,
            'setcdr':  stl.setcdr,
            'cons':    lambda x,y: [x] + y,
            'eq?':     op.is_, 
            'expt':    pow,
            'equal?':  op.eq, 
            'length':  len, 
            'cons':    lambda *x: Types.Cons(x), 
            'cons?':   lambda x: isinstance(x, Types.Cons), 
            'map':     map,
            'max':     max,
            'min':     min,
            'not':     op.not_,
            'null?':   lambda x: x == [], 
            'null':    None, 
            'number?': lambda x: isinstance(x, Types.Number),  
            'print':   print,
            'procedure?': callable,
            'round':   round,
            'symbol?': lambda x: isinstance(x, Types.Symbol),
            })
