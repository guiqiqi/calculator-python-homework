"""main.py"""

import calculator
from ui import UI

def evaluator(expression: str) -> calculator.Number:
    """Calculate expression and return answer."""
    tokens = list(calculator.tokenize(expression))
    calculator.prefixing(tokens)
    calculator.balancing(tokens)
    tokens = list(calculator.shunting(tokens))
    return calculator.evaluate(tokens)


if __name__ == '__main__':
    ui = UI(evaluator)
    ui.mainloop()
