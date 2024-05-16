"""
Course: ADS'4
Lab: 03
"""

import timeit
import numpy as np
import pyinputplus as pyip

from typing import Callable

STATS: dict = {}


class Node:
    """ Node class for DLL"""

    def __init__(self, data):
        self.data = data  # stores actual data
        self.next = None  # pointer for the next node
        self.prev = None  # pointer for the prev node


class DoublyLinkedList:
    """ DLL implementation """

    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_start(self, data):
        new_node = Node(data)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def delete_from_start(self):
        if self.is_empty():
            return None

        data = self.head.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        return data

    def delete_from_end(self):
        if self.is_empty():
            return None

        data = self.tail.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        return data

    def display_forward(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next

    def display_backward(self):
        current = self.tail

        while current:
            print(current.data, end=' ')
            current = current.prev

    def return_forward(self) -> list:
        current = self.head
        temp = []

        while current:
            temp.append(current.data)
            current = current.next

        return temp

    def return_backward(self) -> list:
        current = self.tail
        temp = []

        while current:
            temp.append(current.data)
            current = current.prev

        return temp


def main():
    """ Main entry point """

    print_task_preset()
    inp = pyip.inputCustom(prompt=">> Enter your text:\n", blank=False, customValidationFunc=validate)

    words = inp[:-1].split()
    print(f'[*] You entered {len(words)} word(s).')

    handler(inp, solver_list)
    handler(inp, solver_array)
    handler(inp, solver_dll)


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

    if isinstance(modified_words, DoublyLinkedList) and isinstance(used_words, DoublyLinkedList):
        print(f'\tUsed words: {", ".join(word for word in used_words.return_backward())}')
        print(f'\tFormatted result: {" ".join(word for word in modified_words.return_backward())}')
    else:
        print(f'\tUsed words: {", ".join(word for word in used_words)}')
        print(f'\tFormatted result: {" ".join(word for word in modified_words)}')
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
    """ Solves the task using numpy array """

    words = np.array(inp.strip('.').split())

    temp = np.vectorize(lambda x: len(x) % 2 == 1 and len(x) > 1)
    filtered_words = words[temp(words)]

    modified_word = np.vectorize(lambda x: x[1:-1] + ',')
    modified_words = modified_word(filtered_words)

    return modified_words, filtered_words


def solver_dll(inp: str) -> tuple:
    """ Solves the task using doubly linked list """

    words = inp.strip('.').split()

    used_words = DoublyLinkedList()
    modified_words = DoublyLinkedList()

    for word in words:
        if len(word) % 2 == 1:
            if len(word) > 1:
                used_words.insert_at_start(word.replace('.', '').replace(',', ''))

                modified_word = word[1:-1] + ','
                modified_words.insert_at_start(modified_word)

    return modified_words, used_words


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
