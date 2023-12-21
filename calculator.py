from __future__ import annotations

import enum
import string
import operator
import fractions
import typing as t


Number = fractions.Fraction


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
        try:
            return self.evaluator(*numbers)
        except ZeroDivisionError:
            raise ValueError('cannot divide by zero')


Add = Operator('+', priority=0, evaluator=operator.add)
Sub = Operator('-', priority=0, evaluator=operator.sub)
Mul = Operator('*', priority=1, evaluator=operator.mul)
Div = Operator('/', priority=1, evaluator=operator.truediv)
Mod = Operator('%', priority=1, evaluator=operator.mod)
Pow = Operator('^', priority=3, evaluator=operator.pow)


Token = t.Union[Number, Braket, Operator]


def tokenize(expr: str) -> t.List[Token]:
    """Tokenize user input into tokens.
    This function will try to split all user input into tokens.
    Space char will be ignored.

    Raises: ValueError if occured invalid input or characters.

    Example:
    ```
    >>> tokenize('12+(34*56^3)')
    [12, +, Bracket.L, 34, *, 56, ^, 30, Bracket.R]
    ```
    """
    buffer = []
    result = []
    for partial in expr:

        # Ignore space char
        if partial == ' ':
            continue

        # If input is a number add it to buffer
        if partial in string.digits:
            buffer.append(partial)
            continue

        # Otherwise means we need to given a number from buffer and clear it
        if buffer:
            try:
                result.append(Number(''.join(buffer)))
            except ValueError:
                raise ValueError(f'invalid number: {"".join(buffer)}')
            buffer.clear()

        # If input is not number, check whether is a symbol or braket
        if partial in Operator.Symbols:
            result.append(Operator.Symbols[partial])
            continue
        if partial in [member.value for member in Braket]:
            result.append(Braket(partial))
            continue

        # If all branches not hitted, means illegal input
        raise ValueError(f'invalid input: {partial}')

    # If anything last in buffer, must be a Number
    if buffer:
        try:
            result.append(Number(''.join(buffer)))
        except ValueError:
            raise ValueError(f'invalid number: {"".join(buffer)}')
        buffer.clear()

    return result


def prefixing(tokens: t.List[Token]) -> None:
    """Add prefix 0 to single negative and positive operator.

    '+' and '-' could also be used as positive and negative indicator for a number.
    So once we add another zero once found a '+' or '-' behind a number without another number in front of.
    """
    copied = tokens[::]
    for index, token in enumerate(copied):
        if token is Add or token is Sub:
            if index == 0 or (not isinstance(copied[index - 1], Number)
                              and copied[index - 1] is not Braket.R):
                tokens.insert(index, Number(0))


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


def shunting(tokens: t.List[Token]) -> t.List[Token]:
    """Shunting yard algorithm."""
    result = []
    stack = []
    for token in tokens:
        if isinstance(token, Number):
            result.append(token)

        # Check the priority for Operator liked token
        elif isinstance(token, Operator):
            while (stack and stack[-1] != Braket.L and
                   stack[-1].priority >= token.priority):
                result.append(stack.pop())
            stack.append(token)

        # If token is left bracket, push it directly
        elif token == Braket.L:
            stack.append(token)

        # If token is right bracket, find corresponding left bracket
        elif token == Braket.R:
            while stack and stack[-1] != Braket.L:
                result.append(stack.pop())
            stack.pop()  # Pop the left bracket

    # Get the rest operators
    while stack:
        result.append(stack.pop())
    return result


def evaluate(tokens: t.List[Token]) -> Number:
    """Evaluate Reverse Polish notaion.

    Traverse the entire expression from left to right. 
    If a number is encountered, it is pushed directly onto the stack. 
    If a symbol is encountered, the top two numbers are popped off the stack.

    Example:
    ```
    >>> evaluate([1, 2, -, 4, 5, +, *])  # (1 - 2) * (4 + 5)
    -9.0
    """
    stack = []
    for token in tokens:
        if not isinstance(token, Number) and not isinstance(token, Operator):
            raise ValueError('invalid element exists in RPN')
        if isinstance(token, Number):
            stack.append(token)
            continue
        if isinstance(token, Operator):
            if len(stack) < 2:
                raise ValueError(f'invalid expression during reduce {token}')
            x, y = stack.pop(), stack.pop()
            stack.append(token(y, x))

    # Return answer and check whether still have unused numbers
    try:
        answer = stack.pop()
    except IndexError:
        raise ValueError(f'unkown error with rpn tokens: {tokens}')
    if stack:
        raise ValueError(
            f'invalid expression with redundant number {stack[0]}...')
    return answer


# if __name__ == '__main__':
#     tokens = tokenize('(1.2+8.8)*3^(2/2)+1')
#     prefixing(tokens)
#     balancing(tokens)
#     rpn = shunting(tokens)
#     print(evaluate(rpn))
