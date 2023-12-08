# RPN Calculator with Tkinter UI

##　Introduction
This project is a calculator application that supports Reverse Polish Notation (RPN). It includes a command-line interface for direct RPN conversion and evaluation, along with a graphical user interface (GUI) built using Tkinter. The calculator can handle basic arithmetic operations and is designed to provide an intuitive and efficient calculating experience.

## Features
RPN Conversion: Convert standard arithmetic expressions into Reverse Polish Notation.
Arithmetic Operations: Supports basic operations like addition, subtraction, multiplication, division, and exponentiation.
Tkinter GUI: A simple and user-friendly graphical interface for easy interaction.
Unit Tests: Comprehensive unit tests ensuring the reliability and accuracy of the calculator's core functionalities.

## Installation
To run this application, you need Python installed on your system. This project is developed and tested with Python 3.8, but it should be compatible with other Python 3 versions.

You need to ensure that you Python configured with `Tkinter` support.

- Clone or download the repository to your local machine.
- Navigate to the project directory.
- Install Poetry and create enviroment for this projects: `pip install poetry && poetry install`
- Run calculator with: `poetry run calculator`

For running unittest, run: `poetry run test`