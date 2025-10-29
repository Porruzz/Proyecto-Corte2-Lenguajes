import unittest
from src.syntax.first_follow import compute_first, compute_follow
from src.syntax.grammar_io import load_grammar

class TestFirstFollow(unittest.TestCase):
    def setUp(self):
        self.start, self.G = load_grammar("grammars/ejemplo_p6.g")

    def test_first(self):
        first, _ = compute_first(self.start, self.G)
        self.assertIn('(', first['E'])
        self.assertIn('id', first['T'])

    def test_follow(self):
        _, follow = compute_follow(self.start, self.G)
        self.assertIn(')', follow['E'])
        self.assertIn('$', follow['E'])

if __name__ == "__main__":
    unittest.main()
