import unittest
from src.main import run_parse

class TestParsePython(unittest.TestCase):
    def test_mini_python_ok(self):
        result = run_parse("grammars/python_subset.g", "examples/python/ok/mini.py")
        self.assertEqual(result, 0)

    def test_mini_python_error(self):
        result = run_parse("grammars/python_subset.g", "examples/python/bad/error1.py")
        self.assertNotEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
