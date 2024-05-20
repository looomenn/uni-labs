
import os
from translate import translate

LANG:str = os.getenv('LANG', 'eng')
INDENT: str = '\t\t\t\t'


class CircleQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.head = -1
        self.tail = -1

    def enqueue(self, item):
        if (self.tail + 1) % self.size == self.head:
            print(translate(LANG, 'queues', 'full_queue',
                            'error', True, skip_item=item))
        else:
            if self.head == -1:
                self.head = 0

            self.tail = (self.tail + 1) % self.size
            self.queue[self.tail] = item
            print(translate(LANG,'queues','item_added','add',True, add_item=item))

    def dequeue(self):
        if self.head == -1:
            print(translate(LANG, 'queues', 'empty_queue', 'error', True))

        else:
            tmp = self.queue[self.head]

            if self.head == self.tail:
                self.head = self.tail = -1
            else:
                self.head = (self.head + 1) % self.size

            print(translate(LANG, 'queues', 'item_deleted', 'delete',
                            True, delete_item=tmp))
            return tmp

    def display(self):
        if self.head == -1:
            print(translate(LANG, 'queues', 'empty_queue', 'error', True))
        else:
            if self.tail >= self.head:
                content = self.queue[self.head:self.tail + 1]
                fill = self.tail - self.head + 1
            else:
                content = self.queue[self.head:self.size] + self.queue[0:self.tail + 1]
                fill = self.size - self.head + self.tail + 1

            print(translate(LANG, 'queues', 'queue_status', 'general', True))

            print(translate(LANG, 'queues', 'queue_size',
                            '', False, indent=INDENT, size=self.size))

            print(translate(LANG, 'queues', 'queue_fullness','',
                            False, indent=INDENT, fullness=f'{fill}/{self.size}'))

            print(translate(LANG, 'queues', 'queue_content','',
                            False, indent=INDENT, content=content))
