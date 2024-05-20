
INDENT: str = '\t\t\t\t'


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
