import typing as t

import tkinter
import tkinter.messagebox as msgbox


class InputPad(tkinter.Frame):
    """Input pad on down side.

    [   ans   ]
    -----------
     1 2 3 + /
     4 5 6 - %
     7 8 9 * ^
      0  .  =
    """

    def __init__(
        self,
        master: tkinter.Tk,
        command: t.Callable[[str], None],
        evaluator: t.Callable[[], None],
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.inputs: t.List[str] = []
        self.evalutor = evaluator

        # Number buttons
        numebrs = [tkinter.Button(self, text=f'{n}',
                                  command=lambda n=n: command(str(n)),
                                  height=2, width=3
                                  ) for n in range(10)]
        numebrs[1].grid(row=0, column=0, sticky=tkinter.NSEW)
        numebrs[2].grid(row=0, column=1, sticky=tkinter.NSEW)
        numebrs[3].grid(row=0, column=2, sticky=tkinter.NSEW)
        numebrs[4].grid(row=1, column=0, sticky=tkinter.NSEW)
        numebrs[5].grid(row=1, column=1, sticky=tkinter.NSEW)
        numebrs[6].grid(row=1, column=2, sticky=tkinter.NSEW)
        numebrs[7].grid(row=2, column=0, sticky=tkinter.NSEW)
        numebrs[8].grid(row=2, column=1, sticky=tkinter.NSEW)
        numebrs[9].grid(row=2, column=2, sticky=tkinter.NSEW)
        numebrs[0].grid(row=3, column=0, columnspan=2, sticky=tkinter.NSEW)
        tkinter.Button(self, text='.', command=lambda: command(
            '.')).grid(row=3, column=2, sticky=tkinter.NSEW)

        # Operators buttons
        operators = {s: tkinter.Button(self, text=f'{s}',
                                       height=2, width=3,
                                       command=lambda s=s: command(s))
                     for s in ['+', '-', '*', '/', '^', '%']}
        operators['+'].grid(row=0, column=3, sticky=tkinter.NSEW)
        operators['-'].grid(row=1, column=3, sticky=tkinter.NSEW)
        operators['*'].grid(row=2, column=3, sticky=tkinter.NSEW)
        operators['/'].grid(row=0, column=4, sticky=tkinter.NSEW)
        operators['%'].grid(row=1, column=4, sticky=tkinter.NSEW)
        operators['^'].grid(row=2, column=4, sticky=tkinter.NSEW)
        tkinter.Button(self, text='=', command=evaluator).grid(
            row=3, column=3, columnspan=2, sticky=tkinter.NSEW)


class UI(tkinter.Tk):

    def __init__(self, evaluator: t.Callable[[str], float], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Calculator")
        self.inputs = tkinter.StringVar(self)
        self.resizable = (False, False)
        self.evaluator = evaluator

        buffer = tkinter.Entry(
            self, textvariable=self.inputs, justify=tkinter.RIGHT, font=("Calibri 20"))
        buffer.grid(row=0, column=0, sticky=tkinter.NSEW, ipady=10)

        InputPad(
            self,
            command=lambda s: self.inputs.set(self.inputs.get() + s),
            evaluator=self.calculate
        ).grid(row=2, column=0)

    def calculate(self) -> None:
        """Get expression saved in inputs buffer and """
        expression = self.inputs.get()
        self.inputs.set('')
        try:
            answer = self.evaluator(expression)
            self.inputs.set(str(answer))
        except ValueError as error:
            msgbox.showerror('Invalid expression', error.args[0])
