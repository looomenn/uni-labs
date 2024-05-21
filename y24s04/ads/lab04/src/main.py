"""
Course: ADS'4
Lab: 04
"""

import pyinputplus as pyip

from ListQueue import ListQueue
from CircleQueue import CircleQueue
from translate import translate, tprint

LANG: str = 'eng'
DEBUG: bool = False
INDENT: str = '\t\t\t'
BANNER: str = r""" 
───────────────────────────
ange1o      2024      lab04"""

BANNED_REG = [
    (
        r'[^0-9A-Za-z\s()+\-*/]',
        translate(LANG, 'system', 'nuh', 'error')
    )
]


def home_menu() -> None:
    """
    Main menu handler
    @return: None
    """
    choices: list = [
        translate(LANG, 'menu', 'queue-task', use_prefixes=False),
        translate(LANG, 'menu', 'equation-task', use_prefixes=False),
        translate(LANG, 'menu', 'leave', use_prefixes=False),
    ]

    prompt: str = translate(LANG, 'menu', 'welcome', use_prefixes=False)

    while True:
        print(BANNER)
        choice = pyip.inputMenu(
            choices=choices,
            prompt=prompt,
            numbered=True,
            blank=False,
            default=1
        )

        match choice:
            case _ if choice == choices[0]:
                queue_task_menu()

            case _ if choice == choices[1]:
                equations_task_menu()

            case _ if choice == choices[-1]:
                tprint(LANG, 'menu', 'goodbye', '', use_prefixes=False)
                break

            case _:
                tprint(LANG, 'system', 'nuh', 'error')


def queue_task_menu() -> None:
    """
    Menu handler for queue task
    @return: None
    """

    prompt = translate(LANG, 'queues', 'menu_prompt', '', use_prefixes=False)

    choices: list = [
        translate(LANG, 'queues', 'circular_queue', use_prefixes=False),
        translate(LANG, 'queues', 'list_queue', use_prefixes=False),
        translate(LANG, 'menu', 'return_back', use_prefixes=False),
    ]

    while True:
        print(BANNER)
        choice = pyip.inputMenu(
            choices=choices,
            prompt=prompt,
            numbered=True,
            blank=False
        )

        match choice:
            case _ if choice == choices[0]:

                min_, max_ = 1, 30  # queue size limits
                size_prompt = translate(LANG, 'queues', 'enter_size', 'input', min=min_, max=max_)
                size = pyip.inputInt(prompt=size_prompt, min=min_, max=max_)

                tprint(LANG, 'queues', 'initialized', 'general', size=size)

                queue = CircleQueue(size)
                queue_menu(queue)

            case _ if choice == choices[1]:
                queue = ListQueue()
                queue_menu(queue)

            case _ if choice == choices[-1]:
                tprint(LANG, 'menu', 'return_goodbye', '', use_prefixes=False)
                break

            case _:
                tprint(LANG, 'system', 'nuh', 'error')


def queue_menu(queue: CircleQueue | ListQueue) -> None:
    """
    Menu for controlling the queue
    @param queue: CircleQueue or ListQueue object
    @return:None
    """
    if isinstance(queue, CircleQueue):
        queue_type: str = translate(LANG, 'queues',
                                    'circular_queue', '', use_prefixes=False)
    else:
        queue_type: str = translate(LANG, 'queues', 'list_queue', use_prefixes=False)

    prompt: str = translate(LANG, 'queues', 'control_menu_prompt',
                            use_prefixes=False, type=queue_type)

    choices: list = [
        translate(LANG, 'queues', 'control_menu_add', use_prefixes=False),
        translate(LANG, 'queues', 'control_menu_add_bulk', use_prefixes=False),
        translate(LANG, 'queues', 'control_menu_delete', use_prefixes=False),
        translate(LANG, 'queues', 'control_menu_status', use_prefixes=False),
        translate(LANG, 'menu', 'return_back', use_prefixes=False)
    ]

    while True:
        print(BANNER)
        choice = pyip.inputMenu(choices=choices,
                                prompt=prompt,
                                numbered=True,
                                blank=False)

        match choice:
            case _ if choice == choices[0]:
                add_prompt = translate(LANG, 'system', 'input', 'input')

                item = pyip.inputStr(prompt=add_prompt,
                                     strip=True,
                                     blank=False)
                queue.enqueue(item)

            case _ if choice == choices[1]:
                bulk_prompt = translate(LANG, 'system', 'bulk_input', 'input')
                items = pyip.inputStr(prompt=bulk_prompt, strip=True, blank=False)
                [queue.enqueue(item) for item in items.split()]

            case _ if choice == choices[2]:
                queue.dequeue()

            case _ if choice == choices[3]:
                queue.display()

            case _ if choice == choices[-1]:
                tprint(LANG, 'menu', 'return_goodbye', '', use_prefixes=False)
                break

            case _:
                tprint(LANG, 'system', 'nuh', 'error')


def equations_task_menu() -> None:
    """
    Menu handler for equations task
    @return: None
    """

    choices: list = [
        translate(LANG, 'equations', 'examples', use_prefixes=False),
        translate(LANG, 'equations', 'own_equation', use_prefixes=False),
        translate(LANG, 'menu', 'return_back', use_prefixes=False),
    ]

    prompt: str = translate(LANG, 'equations', 'menu_prompt', use_prefixes=False)

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
                tprint(LANG, 'menu', 'return_goodbye', '', use_prefixes=False)
                break

            case _:
                tprint(LANG, 'system', 'nuh', 'error')


def equation_input_handler() -> None:
    """
    Handles user inputs for equations, converts them to postfix form, and prints the results.

    @return: None
    """

    prompt: str = translate(LANG, 'equations', 'input', 'input')

    equation, equation_type = pyip.inputCustom(
        customValidationFunc=validation,
        prompt=prompt,
        blank=False,
        strip=True,
        blockRegexes=BANNED_REG
    )

    postfix = to_postfix(equation)

    tprint(LANG, 'equations', 'equation', equation=equation)

    tprint(LANG, 'equations', 'postfix_form',
           use_prefixes=False, indent=INDENT, equation=" ".join(postfix))

    if equation_type == 'digits':
        tprint(LANG, 'equations', 'evaluation',
               use_prefixes=False, indent=INDENT, result=evaluate(postfix))


def validation(equation: str) -> (str, str):
    """
    Validates the given equation string in infix form.

    This function checks the structure of the equation to ensure it is valid.

    The following checks are performed:
    - Parentheses are balanced and correctly matched.
    - The equation contains both digits and valid operators.
    - No two operators are consecutive.
    - The equation does not start or end with an operator.
    - The equation does not mix digits and alphabetic characters.
    - The equation is at least 3 characters long and contains at least one operator.

    :param equation: The equation in infix form to be validated.
    :return: The validated equation if all checks pass and equation type (digits or alphabetic)
    :raises pyip.ValidationException: If the equation is invalid according to the checks.
    """

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
                    translate(LANG, 'equations', 'invalid_equation_math', 'error')
                )
            stack.pop()

    if stack:
        raise pyip.ValidationException(
            translate(LANG, 'equations', 'invalid_equation_math', 'error')
        )

    prev_char: str = ''
    for i, char in enumerate(equation):
        if char in operators:
            if i == 0 or i == len(equation) - 1:
                # operator at the beginning or end
                raise pyip.ValidationException(
                    translate(LANG, 'equations', 'invalid_equation_math', 'error')
                )
            if prev_char in operators:
                # two consecutive operators
                raise pyip.ValidationException(
                    translate(LANG, 'equations', 'consecutive_operators', 'error')
                )

        prev_char = char

    if has_digit and has_alpha:
        raise pyip.ValidationException(
            translate(LANG, 'equations', 'invalid_structure', 'error')
        )

    if len(equation) < 3 or not any(op in equation for op in operators):
        raise pyip.ValidationException(
            translate(LANG, 'equations', 'no_operations', 'error')
        )

    equation_type = 'digits' if has_digit else 'alpha'

    return equation, equation_type


def equations_example() -> None:
    """
    Displays predefined equations in both infix and postfix forms, and evaluates them if supported.

    This function defines a set of predefined equations, converts each equation from
    infix form to postfix form, and prints both forms.
    If an equation supports evaluation, it evaluates the postfix form and prints the result.

    :return: None
    """

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

        print('\n')
        tprint(LANG, 'equations', 'equation', equation=infix)

        tprint(LANG, 'equations', 'postfix_form',
               use_prefixes=False, indent=INDENT, equation=" ".join(postfix))

        if equation['supports_evaluation']:
            result = evaluate(postfix)

            tprint(LANG, 'equations', 'evaluation',
                   use_prefixes=False, indent=INDENT, result=result)


def evaluate(postfix):
    """
    Evaluates a postfix (Reverse Polish Notation) expression

    :param postfix: A string of symbols representing the postfix expression.
    :return: The evaluated result of the postfix expression.
    :raises ValueError: If an invalid symbol is encountered in the expression.
    """

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


def to_postfix(equation: str) -> list:
    """
    Converts an infix expression to postfix form (Reverse Polish Notation).
    @param equation: The infix expression to be converted.
    @return: Converted postfix expression
    """
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

    if DEBUG:
        print(f'[EQ][D] {symbols}')

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
            if DEBUG:
                print(f'{symbol=}, {stack=}, {priority[symbol]=}')

            while stack and stack[-1] != '(' and priority[symbol] <= priority[stack[-1]]:
                result.append(stack.pop())
            stack.append(symbol)

    while stack:
        result.append(stack.pop())

    return result


def main() -> None:
    """ main entry point """
    home_menu()


if __name__ == '__main__':
    main()
