"""
Memory was implemented using dicitionary.
"""

import math
import operator as op
import Types
import StandardLibrary as stl
import sys

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

"""
struct BlockHeader { }

V_Memory:
    max heap size;
    header size;

    # Memory allocation interface:
    malloc()
    _request_memory()
    _find_free_block()
    _split_block() if free block is at least twice larger than needed

    # Memory cleaning interface:
    gc(environment)
    _markAll() in environment
    _sweep() through all virtual memory and delete unmarked
"""

class Header:
    def __init__(self, block_size=0):
        self.size = block_size
        self.prev = None
        self.next = None
        self.is_free = True
        self.is_marked = False

        self.data = None

    def set_data(self, data):
        self.data = data

    def __repr__(self):
        return f"size: {self.size} | data: {self.data} | is_free: {self.is_free}"

MAX_HEAP_SIZE = 256
HEADER_SIZE = sys.getsizeof(Header)

class VirtualMemory:
    last_block = None

    def __init__(self):
        self.heap_size = 0
        self.first_obj = None
        self.objects_amount = 0
        self.heap = [None for i in range(MAX_HEAP_SIZE)]
        self.first_block = None

    def malloc(self, size):
        block = None

        if size <= 0:
            return None

        size += HEADER_SIZE
        
        if self.first_block == None:
            block = self.request_memory(size)
            if block == None:
                    return None
            self.first_block = block
        else:
            block = self.find_free_block(self.first_block, size)
            if block == None:
                block = self.request_memory(size)
                if block == None:
                    return None
            else:
                block.is_free = False

        self.heap_size += 1
        self.objects_amount += 1
        self.first_obj = block
        self.heap[self.heap_size+1] = block

        VirtualMemory.last_block = block
        return block
    
    def request_memory(self, size):
        block = Header(size)
        block.next = None
        block.is_free = False

        if VirtualMemory.last_block:
            VirtualMemory.last_block.next = block
            block.prev = VirtualMemory.last_block
        else:
            self.first_block = block

        VirtualMemory.last_block = block    

        return block

    def find_free_block(self, start_block, size):
        current = start_block

        while (current):
            if current.is_free and current.size >= size:
                if current.size >= 2*size:
                    current = self.split_block(current, size)  
                return current
            
            current = current.next

        return None

    def split_block(block, size):
        new_block = Header(block.size - size)
        new_block.next = block.next
        new_block.is_free = True

        block.size = size
        block.next = new_block
        return block

    def gc(self, env):
        reachable_objects = env.values()
        self.markAll(reachable_objects)
        self.sweep()
        self.unmarkAll()

    def markAll(self, objects):
        for obj in objects:
            obj.is_marked = True

    def unmarkAll(self):
        for obj in self.heap:
            obj.is_marked = False

    def sweep(self):
        current = self.first_block

        while (current):
            if (current.is_marked is not True):
                current.data = None
                current.is_free = True
            current = current.next

    def free_block(self, block):
        block.is_free = True
        block.data = None
