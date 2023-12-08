import typing as t

import tkinter
import tkinter.messagebox as msgbox


class InputPad(tkinter.Frame):
    """Input pad on down side.

    [   ans   ]
    -----------
     ( ) <  C
     1 2 3 + /
     4 5 6 - %
     7 8 9 * ^
      0  .  =
    """

    def __init__(
        self,
        master: tkinter.Tk,
        add: t.Callable[[str], None],
        remove: t.Callable[[], None],
        clear: t.Callable[[], None],
        evaluator: t.Callable[[], None],
        *args,
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.inputs: t.List[str] = []
        self.evalutor = evaluator

        # Number buttons
        numebrs = [tkinter.Button(self, text=f'{n}',
                                  command=lambda n=n: add(str(n)),
                                  height=2, width=3
                                  ) for n in range(10)]
        numebrs[1].grid(row=1, column=0, sticky=tkinter.NSEW)
        numebrs[2].grid(row=1, column=1, sticky=tkinter.NSEW)
        numebrs[3].grid(row=1, column=2, sticky=tkinter.NSEW)
        numebrs[4].grid(row=2, column=0, sticky=tkinter.NSEW)
        numebrs[5].grid(row=2, column=1, sticky=tkinter.NSEW)
        numebrs[6].grid(row=2, column=2, sticky=tkinter.NSEW)
        numebrs[7].grid(row=3, column=0, sticky=tkinter.NSEW)
        numebrs[8].grid(row=3, column=1, sticky=tkinter.NSEW)
        numebrs[9].grid(row=3, column=2, sticky=tkinter.NSEW)
        numebrs[0].grid(row=4, column=0, columnspan=2, sticky=tkinter.NSEW)
        tkinter.Button(self, text='.', command=lambda: add(
            '.')).grid(row=4, column=2, sticky=tkinter.NSEW)

        # Operators buttons
        operators = {s: tkinter.Button(self, text=f'{s}',
                                       height=2, width=3,
                                       command=lambda s=s: add(s))
                     for s in ['+', '-', '*', '/', '^', '%']}
        operators['+'].grid(row=1, column=3, sticky=tkinter.NSEW)
        operators['-'].grid(row=2, column=3, sticky=tkinter.NSEW)
        operators['*'].grid(row=3, column=3, sticky=tkinter.NSEW)
        operators['/'].grid(row=1, column=4, sticky=tkinter.NSEW)
        operators['%'].grid(row=2, column=4, sticky=tkinter.NSEW)
        operators['^'].grid(row=3, column=4, sticky=tkinter.NSEW)
        tkinter.Button(self, text='=', command=evaluator).grid(
            row=4, column=3, columnspan=2, sticky=tkinter.NSEW)

        # Add brackets
        tkinter.Button(self, text='(', command=lambda: add('('), height=2).grid(
            row=0, column=0, sticky=tkinter.NSEW)
        tkinter.Button(self, text=')', command=lambda: add(')'), height=2).grid(
            row=0, column=1, sticky=tkinter.NSEW)

        # Add remover and cleaner
        tkinter.Button(self, text='DEL', command=remove, height=2).grid(
            row=0, column=2, sticky=tkinter.NSEW)
        tkinter.Button(self, text='C', command=clear, height=2).grid(
            row=0, column=3, columnspan=2, sticky=tkinter.NSEW)


class UI(tkinter.Tk):

    def __init__(self, evaluator: t.Callable[[str], float], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Calculator")
        self.inputs = tkinter.StringVar(self)
        self.resizable = (False, False)
        self.evaluator = evaluator

        def keypress(event: tkinter.Event) -> None:
            """Filter all key press event and bind event."""
            if event.keysym == 'Return':
                self.calculate()

        def insert(char: str) -> None:
            """Insert a new char to current position."""
            current = self.inputs.get()
            position = self.buffer.index(tkinter.INSERT)
            updated = current[:position] + char + current[position:]
            self.inputs.set(updated)
            self.buffer.icursor(position + 1)

        def remove() -> None:
            """Remove a char in current cursor position."""
            current = self.inputs.get()
            position = self.buffer.index(tkinter.INSERT)
            updated = current[:position - 1] + current[position:]
            self.inputs.set(updated)
            self.buffer.icursor(position - 1)

        buffer = self.buffer = tkinter.Entry(
            self, textvariable=self.inputs, justify=tkinter.RIGHT, font=("Calibri 20"))
        buffer.grid(row=0, column=0, sticky=tkinter.NSEW, ipady=10)
        buffer.bind('<Key>', func=keypress)

        InputPad(
            self,
            add=insert,
            remove=remove,
            clear=lambda: self.inputs.set(''),
            evaluator=self.calculate
        ).grid(row=2, column=0)

        # self.buffer.grab_set()

    def calculate(self) -> None:
        """Get expression saved in inputs buffer and calculate for updating result."""
        expression = self.inputs.get()
        self.inputs.set('')
        try:
            answer = self.evaluator(expression)
            answer = int(answer) if int(answer) == answer else round(answer, 5)
            self.inputs.set(str(answer))
            self.buffer.icursor(len(self.inputs.get()))
        except ValueError as error:
            msgbox.showerror('Invalid expression', error.args[0])
