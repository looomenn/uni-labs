"""
Course: ADS'4
Lab: 03
"""

import array as arr
import pyinputplus as pyip


def main():
    """ Main entry point """

    #inp = pyip.inputStr(prompt="[!] Enter your text:\n", blank=False, applyFunc=validate)
    inp = pyip.inputCustom(prompt="[*] Enter your text:\n", blank=False, customValidationFunc=validate)

    words = inp[:-1].split()
    print(f'[*] You entered {len(words)} word(s).')


def validate(inp: str) -> str:
    """ Validating text input """

    if any(char not in "abcdefghijklmnopqrstuvwxyz .'" for char in inp):
        raise pyip.ValidationException(f'[!] Input must only contain lowercase Latin letters, spaces, and a dot. ')

    if not inp.endswith('.'):
        raise pyip.ValidationException("[!] Input must end with a dot.")

    return inp


if __name__ == '__main__':
    main()
