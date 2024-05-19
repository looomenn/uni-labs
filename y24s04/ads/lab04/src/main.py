"""
Course: ADS'4
Lab: 04
"""

import pyinputplus as pyip

DEBUG: bool = False
INDENT: str = '\t\t\t'
BANNER: str = r"""
───────────────────────────
ange1o      2024      lab04"""


class CircleQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.head = -1
        self.tail = -1

    def enqueue(self, item):
        if (self.tail + 1) % self.size == self.head:
            print(f'[CQ][!] Queue is full, thus {item} won\'t be enqueued')
        else:
            if self.head == -1:
                self.head = 0

            self.tail = (self.tail + 1) % self.size
            self.queue[self.tail] = item
            print(f'[CQ][+] Enqueued: {item}')

    def dequeue(self):
        if self.head == -1:
            print('[CQ][!] Queue is empty')

        else:
            tmp = self.queue[self.head]

            if self.head == self.tail:
                self.head = self.tail = -1
            else:
                self.head = (self.head + 1) % self.size

            print(f'[CQ][-] Dequeued: {tmp}')
            return tmp

    def display(self):
        if self.head == -1:
            print(f'[CQ][!] Queue is empty')
        else:
            if self.tail >= self.head:
                content = self.queue[self.head:self.tail + 1]
                fill = self.tail - self.head + 1
            else:
                content = self.queue[self.head:self.size] + self.queue[0:self.tail + 1]
                fill = self.size - self.head + self.tail + 1

            status = 'full' if (self.tail + 1) % self.size == self.head else f'{fill}/{self.size}'
            print(f'[CQ][*] Queue:')
            print(f'{INDENT}Size: {self.size}')
            print(f'{INDENT}Fullness: {status}')
            print(f'{INDENT}Content: {content}')


class ListQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        print(f'[LQ] Added {item} to the queue')

    def dequeue(self):
        if not self.queue:
            print(f'[LQ][!] Queue is empty')

        else:
            tmp = self.queue.pop(0)
            print(f'[LQ][!] Removed {tmp}')
            return tmp

    def display(self):
        if not self.queue:
            print(f'[LQ][!] Queue is empty')
        else:
            print(f'[LQ] Queue: {self.queue}')


def home_menu():
    """ init user menu """
    while True:
        print(BANNER)
        choice = pyip.inputMenu(['Queue task', 'Equations task', 'Leave (T_T)'],
                                prompt='\nWelcome! Choose your destiny for now:\n',
                                numbered=True,
                                blank=False,
                                default=1)

        match choice:
            case 'Queue task':
                queue_task_menu()
            case 'Leave (T_T)':
                print('Farewell.....')
                break


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


def main():
    """ main entry point """
    home_menu()


if __name__ == '__main__':
    main()
