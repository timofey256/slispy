## **S**imple **LISP** Interpreter in Python.

**Slispy** is a dialect of the LISP programming language, written in Python. It is a simple interpreter that can be installed by cloning the repository and running `python3 src/main.py path=="[PATH to .slispy file]"`.

Slispy provides standard types, including integers, floating-point numbers, booleans, and strings. It also supports lists, lambda functions, conditions, which are a key feature of the LISP programming language.

If you're new to Scheme-like languages and Slispy, be sure to check out the sample programs:

### Program that calculates circle radius.
```
(define circle-area 
	(lambda (r) 
			(* pi (* r r))
  )
) 

(circle-area 3)
```

### Counting how many times number is in the list.
```
(define first car)
(define rest cdr)
(define count
  (lambda (item L)
    (if L (+ (equal? item (first L)) (count item (rest L))) 0)))
(count 0 (list 0 1 2 3 0 0))
```

### Calculating n!
```
(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1)))))) (fact 10)
```

