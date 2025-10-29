import unittest
from src.lexical.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_tokens(self):
        code = "x = 5 + 3"
        lexer = Lexer(code)
        tokens = list(lexer.tokenize())
        expected = ['ID', 'ASSIGN', 'NUM', 'PLUS', 'NUM']
        result = [t.type for t in tokens]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
