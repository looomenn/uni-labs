"""
Course: ADS'4
Lab: 03
"""

import timeit
import numpy as np
import pyinputplus as pyip

from typing import Callable

STATS: dict = {}


def main():
    """ Main entry point """

    print_task_preset()
    inp = pyip.inputCustom(prompt=">> Enter your text:\n", blank=False, customValidationFunc=validate)

    words = inp[:-1].split()
    print(f'[*] You entered {len(words)} word(s).')

    handler(inp, solver_list)
    handler(inp, solver_array)


def validate(inp: str) -> str:
    """ Validating text input """

    inp = inp.lower()

    if any(char not in "abcdefghijklmnopqrstuvwxyz .,'" for char in inp):
        raise pyip.ValidationException(f'[!] Input must only contain lowercase Latin letters, spaces, and a dot. ')

    if not inp.endswith('.'):
        raise pyip.ValidationException("[!] Input must end with a dot.")

    return inp


def handler(inp: str, func: Callable):
    """ Handles text input """

    func_name = func.__name__.replace('_', ' ')

    def time_wrapper():
        return func(inp)

    elapsed_time = timeit.timeit(time_wrapper, number=1)
    modified_words, used_words = func(inp)

    print(f'Solving using {func_name.split()[1]}')
    print(f'[+] Result:')
    print(f'\tUsed words: {", ".join(word for word in used_words):>15}')
    print(f'\tFormatted result: {" ".join(word for word in modified_words):<5}')
    print(f'[!] Time taken: {elapsed_time:6f}\n')


def solver_list(inp: str) -> tuple:
    """ Solves the task using list """

    words = inp.strip('.').split()

    modified_words = []
    used = []

    for word in words:
        if len(word) % 2 == 1:
            if len(word) > 1:

                used.append(word.replace('.', '').replace(',', ''))

                modified_word = word[1:-1] + ','
                modified_words.append(modified_word)

    return modified_words, used


def solver_array(inp: str) -> tuple:
    """ Solves the task using np.array """

    words = np.array(inp.strip('.').split())

    temp = np.vectorize(lambda x: len(x) % 2 == 1 and len(x) > 1)
    filtered_words = words[temp(words)]

    modified_word = np.vectorize(lambda x: x[1:-1] + ',')
    modified_words = modified_word(filtered_words)

    return modified_words, filtered_words


def print_task_preset() -> None:
    """ Prints task """

    banner = r"""
                                              $$\            
                                            $$$$ |           
     $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  \_$$ |  $$$$$$\  
     \____$$\ $$  __$$\ $$  __$$\ $$  __$$\   $$ | $$  __$$\ 
     $$$$$$$ |$$ |  $$ |$$ /  $$ |$$$$$$$$ |  $$ | $$ /  $$ |
    $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|  $$ | $$ |  $$ |
    \$$$$$$$ |$$ |  $$ |\$$$$$$$ |\$$$$$$$\ $$$$$$\\$$$$$$  |
     \_______|\__|  \__| \____$$ | \_______|\______|\______/ 
                        $$\   $$ |                           
                        \$$$$$$  |                           
                         \______/                            


    Program Description:
    This program processes text to find and modify words that have an odd number of characters.
    For each such word, it:
    - Removes the first and last characters,
    - Appends a comma to the end,
    - Outputs the modified word.

    Example Input: "hello world, this is an example of a text."
    Example Output: ["ello,", "his,", "an,", "exampl,"]
    """

    print(banner)


if __name__ == '__main__':
    main()
