from __future__ import annotations

import enum
import string
import operator
import typing as t


Number = float


@enum.unique
class Braket(enum.Enum):
    L = '('
    R = ')'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


class Operator:

    Symbols: t.Dict[str, Operator] = dict()

    def __init__(self, symbol: str, priority: int, evaluator: t.Callable[..., Number]) -> None:
        self.symbol, self.priority = symbol, priority
        self.evaluator = evaluator

        # Check if symbol already defined in symbol dict
        if not symbol in self.Symbols:
            self.Symbols[symbol] = self
        else:
            raise ValueError(f'redefined symbol {symbol}')

    def __repr__(self) -> str:
        return self.symbol

    def __call__(self, *numbers: Number) -> Number:
        """Call function evaluator for returning result."""
        return self.evaluator(*numbers)


Add = Operator('+', priority=0, evaluator=operator.add)
Sub = Operator('-', priority=0, evaluator=operator.sub)
Mul = Operator('*', priority=1, evaluator=operator.mul)
Div = Operator('/', priority=1, evaluator=operator.truediv)
Mod = Operator('%', priority=1, evaluator=operator.mod)
Pow = Operator('^', priority=3, evaluator=operator.pow)


Token = t.Union[Number, Braket, Operator]


def tokenize(expr: str) -> t.Iterator[Token]:
    """Tokenize user input into tokens.
    This function will try to split all user input into tokens.

    Raises: ValueError if occured invalid input or characters.

    Example:
    ```
    >>> tokenize('1.2+(3.4*5.6^3)')
    [1.2, +, Bracket.L, 3.4, *, 5.6, ^, 3.0, Bracket.R]
    ```
    """
    buffer = []
    for partial in expr:

        # If input is a number or dot add it to buffer
        if partial in string.digits + '.':
            buffer.append(partial)
            continue

        # Otherwise means we need to given a number from buffer and clear it
        if buffer:
            try:
                yield (Number(''.join(buffer)))
            except ValueError:
                raise ValueError(f'invalid number: {"".join(buffer)}')
            buffer.clear()

        # If input is not number or dot, check whether is a symbol or braket
        if partial in Operator.Symbols:
            yield Operator.Symbols[partial]
            continue
        if partial in [member.value for member in Braket]:
            yield Braket(partial)
            continue

        # If all branches not hitted, means illegal input
        raise ValueError(f'invalid input: {partial}')


def prefixing(tokens: t.List[Token]) -> None:
    """Add prefix 0 to single negative and positive operator.

    '+' and '-' could also be used as positive and negative indicator for a number.
    So once we add another zero once found a '+' or '-' behind a number without another number in front of.
    """
    for index, token in enumerate(tokens[::]):
        if token is Add or token is Sub:
            if index == 0 or not isinstance(tokens[index - 1], Number):
                tokens.insert(index, Number(0.))


def balancing(tokens: t.List[Token]) -> None:
    """Balancing all brackets.

    Raises: ValueError if occured unbalanced brackets.
    """
    stack = 0
    for index, token in enumerate(tokens):
        if token == Braket.L:
            stack += 1
        if token == Braket.R:
            stack -= 1
        if stack < 0:
            raise ValueError(f'unbalanced bracket at position {index}')
    if stack != 0:
        raise ValueError(f'unbalanced bracket at position {len(tokens)}')


def shunting(tokens: t.List[Token]) -> t.Iterator[Token]:
    """Shunting yard algorithm."""
    ...



if __name__ == '__main__':
    tokens = list(tokenize('1.2+(3.4*52^3)'))
    prefixing(tokens)
    balancing(tokens)
    print(tokens)