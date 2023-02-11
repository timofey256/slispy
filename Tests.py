import unittest
from Parser import Tokenizer
from Parser import Parser

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

    # def test_tokenize_string(self):
    #     expression = '("hello world")'
    #     expected_tokens = ['(', '"hello world"', ')']
    #     self.assertEqual(tokenize(expression), expected_tokens)

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

    # def test_parse_string(self):
    #     tokens = ['(', '"hello world"', ')']
    #     expected_ast = '"hello world"'
    #     self.assertEqual(parse(tokens), expected_ast)

    def test_parse_symbol(self):
        tokens = ['(', 'define', 'x', '10', ')']
        expected_ast = ['define', 'x', 10]
        p = Parser()
        self.assertEqual(p.parse(tokens), expected_ast)

if __name__ == '__main__':
    unittest.main()
