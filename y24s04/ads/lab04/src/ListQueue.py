""" ListQueue implementation """


import os
from translate import translate

LANG:str = os.getenv('LANG', 'eng')


class ListQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        print(translate(LANG,'queues','item_added','add',True, add_item=item))

    def dequeue(self):
        if not self.queue:
            print(translate(LANG,'queues','empty_queue','error',True))

        else:
            tmp = self.queue.pop(0)
            print(translate(LANG, 'queues', 'item_deleted', 'delete',
                            True, delete_item=tmp))
            return tmp

    def display(self):
        if not self.queue:
            print(translate(LANG,'queues','empty_queue','error',True))
        else:
            print(f'[LQ] Queue: {self.queue}')