"""
Course: ADS'4
Lab: 04
"""

import os
import pyinputplus as pyip

from translate import translate
from CircleQueue import CircleQueue
from ListQueue import ListQueue

LANGUAGE: str = 'ukr'
DEBUG: bool = True
INDENT: str = '\t\t\t\t'
BANNER: str = r"""
───────────────────────────
ange1o      2024      lab04"""

BANNED_REG = [
    (
        r'[^0-9A-Za-z\s()+\-*/]',
        translate(
            LANGUAGE,
            'system',
            'error',
            'nuh'
        )
    )
]


def home_menu():
    """ init user menu """
    choices: list = [
        translate(LANGUAGE, 'menu', 'queue-task', use_prefixes=False),
        translate(LANGUAGE, 'menu', 'equation-task', use_prefixes=False),
        translate(LANGUAGE, 'menu', 'leave', use_prefixes=False),
    ]

    prompt: str = translate(LANGUAGE, 'menu', 'welcome', use_prefixes=False)

    while True:
        print(BANNER)
        choice = pyip.inputMenu(choices=choices,
                                prompt=prompt,
                                numbered=True,
                                blank=False,
                                default=1)

        match choice:
            case _ if choice == choices[0]:
                queue_task_menu()

            case  _ if choice == choices[1]:
                equations_task_menu()

            case  _ if choice == choices[2]:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))
                break

            case _:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))


def queue_task_menu():
    prompt = '\n>> Queue task\nYou are almost there! Select the type of the queue to use!\n'

    while True:
        print(BANNER)
        choice = pyip.inputMenu(['Circular', 'List', 'Leave .______.'],
                                prompt=prompt,
                                numbered=True,
                                blank=False)

        match choice:
            case 'Circular':
                size = pyip.inputInt('Enter queue size ^_+ (min: 1, max: 30): ', min=1, max=30)
                queue = CircleQueue(size)

                print(f"Initialised the circular queue with size: {size}")
                queue_menu(queue)

            case 'List':
                queue = ListQueue()
                queue_menu(queue)

            case 'Leave .______.':
                print('Wrapping things up..')
                break

            case _:
                print("Nuh.. that won't work :( ")


def queue_menu(queue: CircleQueue | ListQueue):
    prompt: str = '\n>> Queue menu:\n'

    while True:
        print(BANNER)
        choice = pyip.inputMenu(['Enqueue',
                                 'Bulk enqueue',
                                 'Dequeue',
                                 'Display Queue',
                                 '<-- Back to menu'
                                 ],
                                prompt=prompt,
                                numbered=True)

        match choice:
            case 'Enqueue':
                item = pyip.inputStr("Enter the item to enqueue: ",
                                     strip=True,
                                     blank=False)
                queue.enqueue(item)

            case 'Bulk enqueue':
                items = pyip.inputStr("Enter the items to enqueue, separated by spaces: ")
                [queue.enqueue(item) for item in items.split()]

            case 'Dequeue':
                queue.dequeue()

            case 'Display Queue':
                queue.display()

            case '<-- Back to menu':
                break

            case _:
                print('Nuh uh..')


def equations_task_menu():
    """ menu handler for equations task """

    prompt: str = '\n>> Equations task:\n'

    while True:
        print(BANNER)
        choice = pyip.inputMenu(['Examples', 'Enter own equation', '<-- Back to menu'],
                                prompt=prompt,
                                numbered=True,
                                blank=False)
        match choice:
            case 'Examples':
                equations_example()
            case 'Enter own equation':
                equation_input_handler()
            case '<-- Back to menu':
                print('Ok... You\'re the captain')
                break
            case _:
                print("Nuh.. that won't work :( ")


def equation_input_handler():
    """ handles user inputs for equations """

    prompt: str = translate(
        LANGUAGE,
        'equations',
        'input',
        'input'
    )

    while True:
        equation = pyip.inputCustom(customValidationFunc=validation,
                                    prompt=prompt,
                                    blank=False,
                                    strip=True,
                                    blockRegexes=BANNED_REG)
        print(equation)


def validation(equation: str) -> str:
    stack = []
    operators: str = '+-*/'

    has_digit = any(char.isdigit() for char in equation)
    has_alpha = any(char.isalpha() for char in equation)

    for char in equation:
        if char == '(':
            stack.append(char)

        elif char == ')':
            if not stack or stack[-1] != '(':
                raise pyip.ValidationException(
                    translate(
                        LANGUAGE,
                        'equations',
                        'error',
                        'invalid_equation_math'
                    )
                )
            stack.pop()

    if stack:
        raise pyip.ValidationException(
            translate(
                LANGUAGE,
                'equations',
                'error',
                'invalid_equation_math'
            )
        )

    prev_char: str = ''
    for i, char in enumerate(equation):
        if char in operators:
            if i == 0 or i == len(equation) - 1:
                # operator at the beginning or end
                raise pyip.ValidationException(
                    translate(
                        LANGUAGE,
                        'equations',
                        'error',
                        'invalid_equation_math'
                    )
                )
            if prev_char in operators:
                # two consecutive operators
                raise pyip.ValidationException(
                    translate(
                        LANGUAGE,
                        'equations',
                        'error',
                        'consecutive_operators'
                    )
                )
        prev_char = char

    if has_digit and has_alpha:
        raise pyip.ValidationException(
            translate(
                LANGUAGE,
                'equations',
                'error',
                'invalid_structure'
            )
        )

    if len(equation) < 3 or not any(op in equation for op in operators):
        raise pyip.ValidationException(
            translate(
                LANGUAGE,
                'equations',
                'error',
                'no_operations'
            )
        )

    return equation


"""
def validate(inp: str) -> str:

    inp = inp.lower()

    if any(char not in "abcdefghijklmnopqrstuvwxyz .,'" for char in inp):
        raise pyip.ValidationException(f'[!] Input must only contain lowercase Latin letters, spaces, and a dot. ')

    if not inp.endswith('.'):
        raise pyip.ValidationException("[!] Input must end with a dot.")

    return inp

"""


def equations_example():
    """ example handler for equations """

    equations_: dict = {
        'eq1': {
            'infix': '(((A - B) * C) + (D / (E + F)))',
            'supports_evaluation': False
        },
        'eq3': {
            'infix': '(А-B-С)/D-E*F',
            'supports_evaluation': False
        },
        'eq4': {
            'infix': '(A+B)*C-(D+E)/F',
            'supports_evaluation': False
        },
        'eq5': {
            'infix': 'A/(B-C)+D*(E-F)',
            'supports_evaluation': False
        },
        'eq6': {
            'infix': '(A*B+C)/D-F/E',
            'supports_evaluation': False
        },
        'eq7': {
            'infix': '(1 + 2) * 4',
            'supports_evaluation': True
        }
    }

    for key, equation in equations_.items():
        infix = equation['infix']
        postfix = to_postfix(infix)

        print(f'[EQ] Equation: {infix}')
        print(f'{INDENT}Postfix form: {" ".join(postfix)}')

        if equation['supports_evaluation']:
            result = evaluate(postfix)
            print(f'{INDENT}Evaluation: {result}')
        else:
            print(f'{INDENT}Evaluation: equal to infix form')


def evaluate(postfix):
    """ evaluate postfix """

    result = 0
    stack: list = []

    for symbol in postfix:
        if symbol.isdigit():
            stack.append(int(symbol))

        elif symbol.isalpha():
            stack.append(symbol)

        else:
            right = stack.pop()
            left = stack.pop()

            match symbol:
                case '+':
                    result = left + right
                case '-':
                    result = left - right
                case '*':
                    result = left * right
                case '/':
                    result = left / right

            stack.append(result)

    return stack[0]


def to_postfix(equation):
    """ converts infix to postfix form """
    priority: dict = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack: list = []
    result: list = []
    symbols: list = []

    i = 0
    while i < len(equation):
        if equation[i].isalnum():
            j = i
            while j < len(equation) and equation[j].isalnum():
                j += 1
            symbols.append(equation[i:j])
            i = j
        elif equation[i] in "+-*/()":
            symbols.append(equation[i])
            i += 1
        else:
            i += 1

    if DEBUG: print(f'[EQ][D] {symbols}')

    for symbol in symbols:  # If the token is an operand (digit), add it to the output
        if symbol.isalnum():
            result.append(symbol)
        elif symbol == '(':  # If the token is '(', push it onto the stack
            stack.append(symbol)

        elif symbol == ')':  # If the symbol is ')', pop and output from the stack until '(' is found
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # pops ( from the stack

        else:  # handling operators
            if DEBUG: print(f'{symbol=}, {stack=}, {priority[symbol]=}')
            while stack and stack[-1] != '(' and priority[symbol] <= priority[stack[-1]]:
                result.append(stack.pop())
            stack.append(symbol)

    while stack:
        result.append(stack.pop())

    return result


def main():
    """ main entry point """
    home_menu()


if __name__ == '__main__':
    main()
