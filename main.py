"""Calculator in RPN."""

import calculator
from ui import UI


def evaluator(expression: str) -> str:
    """Calculate expression and return answer."""
    print(f'Expression: {expression}')
    tokens = list(calculator.tokenize(expression))
    print(f'Tokenized: {tokens}')
    calculator.prefixing(tokens)
    calculator.balancing(tokens)
    print(f'Validated tokens: {tokens}')
    tokens = list(calculator.shunting(tokens))
    print(f'RPN tokens: {tokens}')
    return str(calculator.evaluate(tokens))


def run() -> None:
    """Run calculator."""
    ui = UI(evaluator)
    ui.mainloop()


if __name__ == '__main__':
    run()
