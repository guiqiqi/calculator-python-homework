import unittest


def suite() -> unittest.TestSuite:
    """Return all unittest suite."""
    from . import test_calculator

    testcases = [
        test_calculator.TestCalculator
    ]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for testcase in testcases:
        suite.addTests(loader.loadTestsFromTestCase(testcase))
    return suite


def run() -> None:
    """Run all unittests."""
    runner = unittest.TextTestRunner()
    runner.run(suite())
