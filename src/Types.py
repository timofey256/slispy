"""
Types which are used in this Lisp-like language implementation.
"""

Symbol = str
List = list
Number = (int, float)
Atom = (Symbol, Number)
Exp = (Atom, List)