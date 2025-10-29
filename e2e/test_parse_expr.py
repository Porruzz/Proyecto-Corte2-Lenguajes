import unittest
from src.main import run_parse

class TestParseExpr(unittest.TestCase):
    def test_expression_ok(self):
        result = run_parse("grammars/ejemplo_p6.g", "examples/python/ok/expresion1.txt")
        self.assertEqual(result, 0)  # 0 = éxito

if __name__ == "__main__":
    unittest.main()
