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

There is also a [list](list_of_functions.md) of standard functions of this Scheme dialect

## How it works?
The Scheme language interpreter is a program that reads and executes Scheme code. The interpreter is written in Python and works by tokenizing the program's text, parsing it, and then running the `eval()` function to execute the program.

### Tokenization **(src/Parser.py)**:
Tokenization is the process of breaking up the input text into meaningful chunks called tokens. The interpreter first reads the input text and tokenizes it by separating it into individual words, numbers, parentheses, and other symbols. It then stores these tokens in a list for further processing.

### **Parsing (src/Parser.py):**
Parsing code involves analyzing the tokens (as generated by the tokenizer) and building a parse tree that represents the structure of the program. The parse tree is built using a recursive descent parser, which works by recursively parsing each subexpression and building up the parse tree from the bottom up.

### **Evaluation (src/Eval.py):**

Evaluation is the process of executing the program. The interpreter uses the `eval()` function to evaluate each expression in the parse tree. The `eval()` function takes an expression and returns its value.

### **Memory (src/Environment.py and stc/VirtualMemory.py):**

The Scheme interpreter implemented in Python uses Environments (which can be imagined as current scopes or contexts) and Virtual Memory to manage variable bindings and data storage efficiently. Environments are responsible for managing variable bindings (they are implemented using dictionaries simply by storing (variable name : index in VM heap) pairs), while Virtual Memory stores heap-allocated memory. Consequently, the interpreter can access memory through current Environment by requesting it value of some variable.

Additionally, the interpreter employs a mark-and-sweep garbage collector to manage memory allocation and deallocation. The garbage collector periodically scans Virtual Memory to free up memory used by unreachable data objects. When the interpreter needs to create a new object and memory is insufficient, the garbage collector is triggered to free up memory by collecting garbage objects.

### **Usage:**

To use the interpreter, simply run the Python script by executing `python3 src/main.py path=="[PATH to .slispy file]"` and enter Scheme code at the prompt. The interpreter will read and execute the code, displaying the result.

### **Limitations:**

The interpreter has a number of limitations, including a lack of support for complex data types, limited error handling, and a lack of optimization. However, it provides a simple and flexible way to experiment with Scheme code and learn the basics of programming language implementation.


