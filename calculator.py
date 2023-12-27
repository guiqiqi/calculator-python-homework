from __future__ import annotations

import enum
import string
import operator
import typing as t

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

class Fraction:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        gcd_value = gcd(numerator, denominator)
        self.numerator = numerator // gcd_value
        self.denominator = denominator // gcd_value

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for +: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for -: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for *: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for /: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)

    def __mod__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for %: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = (self.numerator * other.denominator) % (self.denominator * other.numerator)
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __pow__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type(s) for **: 'Fraction' and '{}'".format(type(other).__name__))
        numerator = self.numerator ** other.numerator
        denominator = self.denominator ** other.denominator
        return Fraction(numerator, denominator)

    def __str__(self):
        return "{}/{}".format(self.numerator, self.denominator)

    def __repr__(self):
        return "Fraction({}, {})".format(self.numerator, self.denominator)
    
Number = Fraction



@enum.unique
class Braket(enum.Enum):#&
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


# Функции для вычисления операций с дробями
def add_fractions(a, b):
    return a + b

def subtract_fractions(a, b):
    return a - b

def multiply_fractions(a, b):
    return a * b

def divide_fractions(a, b):
    return a / b

def modulo_fractions(a, b):
    return a % b

def power_fractions(a, b):
    return a ** b

# Создание операторов с помощью класса Operator
Add = Operator('+', 0, add_fractions)
Sub = Operator('-', 0, subtract_fractions)
Mul = Operator('*', 1, multiply_fractions)
Div = Operator('/', 1, divide_fractions)
Mod = Operator('%', 2, modulo_fractions)
Pow = Operator('^', 3, power_fractions)



Token = t.Union[Number, Braket, Operator]


def tokenize(expr: str) -> t.List[Token]:
    buffer = []
    result = []
    for partial in expr:
        if partial == ' ':
            continue
        if partial in string.digits + '.':
            buffer.append(partial)
            continue
        if buffer:
            try:
                result.append(Number(int(''.join(buffer))))
            except ValueError:
                raise ValueError(f'invalid number: {"".join(buffer)}')
            buffer.clear()
        if partial in Operator.Symbols:
            result.append(Operator.Symbols[partial])
            continue
        if partial in [member.value for member in Braket]:
            result.append(Braket(partial))
            continue
        raise ValueError(f'invalid input: {partial}')
    if buffer:
        try:
            result.append(Number(int(''.join(buffer))))
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
            if index == 0 or not isinstance(copied[index - 1], Number):
                tokens.insert(index, Number(0,1))


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
    answer = stack.pop()
    if stack:
        raise ValueError(
            f'invalid expression with redundant number {stack[0]}...')
    return answer

"""""
if __name__ == '__main__':
    tokens = tokenize('(-9 + 3) * 2')
    prefixing(tokens)
    balancing(tokens)
    print(tokens)
    rpn = shunting(tokens)
    print(rpn)
    print(evaluate(rpn))"""
