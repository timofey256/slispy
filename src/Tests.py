import unittest

from Parser import Tokenizer
from Parser import Parser
from Eval import eval, Procedure
from Environment import Environment

class TestSchemeTokenizer(unittest.TestCase):
    def test_tokenize_simple_expression(self):
        expression = "(+ 2 3)"
        expected_tokens = ['(', '+', '2', '3', ')']
        t = Tokenizer()
        self.assertEqual(t.tokenize(expression), expected_tokens)

    def test_tokenize_nested_expression(self):
        expression = "(* (+ 2 3) 4)"
        expected_tokens = ['(', '*', '(', '+', '2', '3', ')', '4', ')']
        t = Tokenizer()
        self.assertEqual(t.tokenize(expression), expected_tokens)

    def test_tokenize_quote_expression(self):
        expression = "(quote (1 2 3))"
        expected_tokens = ['(', 'quote', '(', '1', '2', '3', ')', ')']
        t = Tokenizer()
        self.assertEqual(t.tokenize(expression), expected_tokens)
        
    def test_tokenize_symbol(self):
        expression = "(define x 10)"
        expected_tokens = ['(', 'define', 'x', '10', ')']
        t = Tokenizer()
        self.assertEqual(t.tokenize(expression), expected_tokens)

class TestSchemeParser(unittest.TestCase):

    def test_parse_simple_expression(self):
        tokens = ['(', '+', '2', '3', ')']
        expected_ast = ['+', 2, 3]
        p = Parser()
        self.assertEqual(p.parse(tokens), expected_ast)

    def test_parse_nested_expression(self):
        tokens = ['(', '*', '(', '+', '2', '3', ')', '4', ')']
        expected_ast = ['*', ['+', 2, 3], 4]
        p = Parser()
        self.assertEqual(p.parse(tokens), expected_ast)

    def test_parse_quote_expression(self):
        tokens = ['(', 'quote', '(', '1', '2', '3', ')', ')']
        expected_ast = ['quote', [1, 2, 3]]
        p = Parser()
        self.assertEqual(p.parse(tokens), expected_ast)

    def test_parse_symbol(self):
        tokens = ['(', 'define', 'x', '10', ')']
        expected_ast = ['define', 'x', 10]
        p = Parser()
        self.assertEqual(p.parse(tokens), expected_ast)

class EvalTestCase(unittest.TestCase):
    def get_AST(self, expression : str):
        t = Tokenizer()
        p = Parser()
        return p.parse(t.tokenize(expression))

    def test_numbers(self):
        self.assertEqual(eval(self.get_AST("1")), 1)
        self.assertEqual(eval(self.get_AST("-1")), -1)
        self.assertEqual(eval(self.get_AST("3.14")), 3.14)
        
    def test_addition(self):
        self.assertEqual(eval(self.get_AST("(+ 1 2)")), 3)
        self.assertEqual(eval(self.get_AST("(+ 1 (+ 2 3))")), 6)
        
    def test_subtraction(self):
        self.assertEqual(eval(self.get_AST("(- 1 2)")), -1)
        self.assertEqual(eval(self.get_AST("(- 7 3)")), 4)
        
    def test_multiplication(self):
        self.assertEqual(eval(self.get_AST("(* 2 3)")), 6)
        self.assertEqual(eval(self.get_AST("(* 2 (* 3 4))")), 24)
        
    def test_division(self):
        self.assertEqual(eval(self.get_AST("(/ 8 2)")), 4)
        self.assertEqual(eval(self.get_AST("(/ 21 7)")), 3)
        
    def test_combined_operations(self):
        self.assertEqual(eval(self.get_AST("(+ (* 2 3) (/ 6 2))")), 9)

    def test_lambda_functions(self):
        self.assertEqual(eval(self.get_AST("((define circle-area (lambda (r) (* pi (* r r)))) (circle-area 3))")), 28.274333882308138)
        self.assertEqual(eval(self.get_AST("((define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1)))))) (fact 10))")), 3628800)
        self.assertEqual(eval(self.get_AST("""(                 
        (define first car) 
        (define rest cdr) 
        (define count (lambda (item L) (if L (+ (equal? item (first L)) (count item (rest L))) 0)))
        (count 0 (list 0 1 2 3 0 0))
        )""")), 3)
        self.assertEqual(list(eval(self.get_AST("""(                 
        (define range (lambda (a b) (if (= a b) (quote ()) (cons a (range (+ a 1) b)))))
        (range 0 10)
        )"""))), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

class TestMemoryManagement(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.env = Environment()
        self.t = Tokenizer()
        self.p = Parser()

    def get_AST(self, expression : str):
        return self.p.parse(self.t.tokenize(expression))

    def test_variable_initialization(self):
        var = 5
        self.env.set_var("var", var)
        self.assertEqual(self.env.get_var("var"), var)

    def test_gc(self):
        var2 = 10
        inner_env = Environment((), (), self.env)
        inner_env.set_var("var2", var2)
        self.env.force_gc()
        try:
            inner_env.get_var("var2")
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_gc2(self):
        self.env.force_gc()
        var3 = eval(self.get_AST("(* 2 3)"), self.env)
        inner_env = Environment((), (), self.env)
        inner_env.set_var("var3", var3)
        self.env.force_gc()
        try:
            inner_env.get_var("var3")
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)
        
    def test_procedure_scope_with_forced_gc(self):
        f = Procedure("r", ["*", "r", 5], self.env)
        self.env.set_var("function", f)
        self.env.force_gc()
        getted = self.env.get_var("function")
        self.assertEqual(getted(3), 15)

if __name__ == '__main__':
    unittest.main(verbosity=2)