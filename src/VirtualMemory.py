import sys

class VM_Manager:
    __vm = None
    def get_instance():
        if not VM_Manager.__vm:
            VM_Manager.__vm = _VirtualMemory()
        
        return VM_Manager.__vm

class _Block:
    def __init__(self, block_size=0):
        # Header part
        self.size = block_size
        self.prev = None
        self.next = None
        self.is_free = True
        self.is_marked = False
        
        # Data part
        self.data = None

    def set_data(self, data):
        self.data = data

    def __repr__(self):
        return f"[size: {self.size} | data: {self.data} | is_free: {self.is_free}]"

MAX_HEAP_SIZE = 256
HEADER_SIZE = sys.getsizeof(_Block)

class _VirtualMemory:
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
        self.heap[self.heap_size-1] = block

        _VirtualMemory.last_block = block
        
        index = self.heap_size-1
        return (block, index)
    
    def request_memory(self, size):
        block = _Block(size)
        block.next = None
        block.is_free = False

        if _VirtualMemory.last_block:
            _VirtualMemory.last_block.next = block
            block.prev = _VirtualMemory.last_block
        else:
            self.first_block = block

        _VirtualMemory.last_block = block    

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
        new_block = _Block(block.size - size)
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

    def markAll(self, indices):
        for index in indices:
            block = self.heap[index]
            block.is_marked = True

    def unmarkAll(self):
        for obj in self.heap:
            if obj is not None:
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
        