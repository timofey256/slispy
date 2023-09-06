def setcar(x, value):
    x.car = value
    return x

def setcdr(x, value):
    x.cdr = value
    return x

def logical_or(*args):
    res = False
    for arg in args:
        res = res or arg

    return res

def logical_and(*args):
    res = True
    for arg in args:
        res = res and arg

    return res