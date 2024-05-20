"""
Course: ADS'4
Lab: 04
"""

import pyinputplus as pyip

from CircleQueue import CircleQueue
from ListQueue import ListQueue
from translate import translate

LANGUAGE: str = 'eng'
DEBUG: bool = False
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

            case _ if choice == choices[1]:
                equations_task_menu()

            case _ if choice == choices[-1]:
                print(translate(LANGUAGE, 'menu', 'goodbye', '', use_prefixes=False))
                break

            case _:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))


def queue_task_menu():
    prompt = translate(LANGUAGE, 'queues', 'menu_prompt', '', use_prefixes=False)

    choices: list = [
        translate(LANGUAGE, 'queues', 'circular_queue', use_prefixes=False),
        translate(LANGUAGE, 'queues', 'list_queue', use_prefixes=False),
        translate(LANGUAGE, 'menu', 'return_back', use_prefixes=False),
    ]

    while True:
        print(BANNER)
        choice = pyip.inputMenu(choices=choices,
                                prompt=prompt,
                                numbered=True,
                                blank=False)

        match choice:
            case _ if choice == choices[0]:

                min_, max_ = 1, 30  # queue size limits

                size_prompt = translate(LANGUAGE, 'queues', 'enter_size', 'input', min=min_, max=max_)
                size = pyip.inputInt(prompt=size_prompt, min=min_, max=max_)
                queue = CircleQueue(size)

                print(translate(LANGUAGE, 'queues', 'initialized', 'general', size=size))
                queue_menu(queue)

            case _ if choice == choices[1]:
                queue = ListQueue()
                queue_menu(queue)

            case _ if choice == choices[-1]:
                print(translate(LANGUAGE, 'menu', 'return_goodbye', '', use_prefixes=False))
                break

            case _:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))


def queue_menu(queue: CircleQueue | ListQueue):
    if isinstance(queue, CircleQueue):
        queue_type: str = translate(LANGUAGE, 'queues',
                                    'circular_queue', '', use_prefixes=False)
    else:
        queue_type: str = translate(LANGUAGE, 'queues', 'list_queue', use_prefixes=False)

    prompt: str = translate(LANGUAGE, 'queues', 'control_menu_prompt',
                            use_prefixes=False, type=queue_type)

    choices: list = [
        translate(LANGUAGE, 'queues', 'control_menu_add', use_prefixes=False),
        translate(LANGUAGE, 'queues', 'control_menu_add_bulk', use_prefixes=False),
        translate(LANGUAGE, 'queues', 'control_menu_delete', use_prefixes=False),
        translate(LANGUAGE, 'queues', 'control_menu_status', use_prefixes=False),
        translate(LANGUAGE, 'menu', 'return_back', use_prefixes=False)
    ]

    while True:
        print(BANNER)
        choice = pyip.inputMenu(choices=choices,
                                prompt=prompt,
                                numbered=True,
                                blank=False)

        match choice:
            case _ if choice == choices[0]:
                add_prompt = translate(LANGUAGE, 'system', 'input', 'input')

                item = pyip.inputStr(prompt=add_prompt,
                                     strip=True,
                                     blank=False)
                queue.enqueue(item)

            case _ if choice == choices[1]:
                bulk_prompt = translate(LANGUAGE, 'system', 'bulk_input', 'input')
                items = pyip.inputStr(prompt=bulk_prompt, strip=True, blank=False)
                [queue.enqueue(item) for item in items.split()]

            case _ if choice == choices[2]:
                queue.dequeue()

            case _ if choice == choices[3]:
                queue.display()

            case _ if choice == choices[-1]:
                print(translate(LANGUAGE, 'menu', 'return_goodbye', '', use_prefixes=False))
                break

            case _:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))


def equations_task_menu():
    """ menu handler for equations task """

    choices: list = [
        translate(LANGUAGE, 'equations', 'examples', use_prefixes=False),
        translate(LANGUAGE, 'equations', 'own_equation', use_prefixes=False),
        translate(LANGUAGE, 'menu', 'return_back', use_prefixes=False),
    ]

    prompt: str = translate(LANGUAGE, 'equations', 'menu_prompt', use_prefixes=False)

    while True:
        print(BANNER)
        choice = pyip.inputMenu(choices=choices,
                                prompt=prompt,
                                numbered=True,
                                blank=False)
        match choice:
            case _ if choice == choices[0]:
                equations_example()
            case _ if choice == choices[1]:
                equation_input_handler()
            case _ if choice == choices[-1]:
                print(translate(LANGUAGE, 'menu', 'return_goodbye', '', use_prefixes=False))
                break

            case _:
                print(translate(LANGUAGE, 'system', 'nuh', 'error'))


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


def equations_example():
    """ example handler for equations """

    equations: dict = {
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

    for key, equation in equations.items():
        infix = equation['infix']
        postfix = to_postfix(infix)

        print(translate(LANGUAGE, 'equations',
                        'equation', 'general', equation=infix))

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

    for symbol in symbols:  # if the symbol is an operand (digit), add it to the output
        if symbol.isalnum():
            result.append(symbol)
        elif symbol == '(':  # if the symbol is '(', push it onto the stack
            stack.append(symbol)

        elif symbol == ')':  # if the symbol is ')', pop and output from the stack until '(' is found
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
