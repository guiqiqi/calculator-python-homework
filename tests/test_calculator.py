import unittest

import calculator as _calc


class TestCalculator(unittest.TestCase):

    def test_tokenize_simple(self):
        self.assertEqual(_calc.tokenize("1 + 2"), [1.0, _calc.Add, 2.0])

    def test_tokenize_complex(self):
        self.assertEqual(_calc.tokenize("1.2 + (3.4 * 5.6)"),
                         [1.2, _calc.Add, _calc.Braket.L, 3.4, _calc.Mul, 5.6, _calc.Braket.R])

    def test_tokenize_invalid_char(self):
        with self.assertRaises(ValueError):
            _calc.tokenize("1 + a")

    def test_tokenize_empty(self):
        self.assertEqual(_calc.tokenize(""), [])

    def test_prefixing_simple(self):
        tokens = _calc.tokenize("-1 + 2")
        _calc.prefixing(tokens)
        self.assertEqual(tokens, [0.0, _calc.Sub, 1.0, _calc.Add, 2.0])

    # Tests for balancing
    def test_balancing_unbalanced(self):
        with self.assertRaises(ValueError):
            tokens = _calc.tokenize("(1 + 2")
            _calc.balancing(tokens)

    def test_balancing_balanced(self):
        tokens = _calc.tokenize("(1 + 2)")
        _calc.balancing(tokens)
        self.assertEqual(tokens, [_calc.Braket.L, 1.0, _calc.Add, 2.0, _calc.Braket.R])

    # Tests for shunting
    def test_shunting_simple(self):
        tokens = _calc.tokenize("1 + 2")
        rpn = _calc.shunting(tokens)
        self.assertEqual(rpn, [1.0, 2.0, _calc.Add])

    # Tests for evaluate
    def test_evaluate_simple(self):
        rpn = [1.0, 2.0, _calc.Add]
        self.assertEqual(_calc.evaluate(rpn), 3.0)

    def test_evaluate_complex(self):
        tokens = _calc.tokenize("3 + 4 * 2 / ( 1 - 5 ) ^ 2")
        rpn = _calc.shunting(tokens)
        self.assertAlmostEqual(_calc.evaluate(rpn), 3)


if __name__ == '__main__':
    unittest.main()
