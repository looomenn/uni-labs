""" ListQueue implementation """

import os
from translate import translate, tprint

LANG: str = os.getenv('LANG', 'eng')
INDENT: str = '\t\t\t\t'


class ListQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        tprint(LANG, 'queues', 'item_added', 'add', True, add_item=item)

    def dequeue(self):
        if not self.queue:
            tprint(LANG, 'queues', 'empty_queue', 'error', True)

        else:
            tmp = self.queue.pop(0)
            tprint(LANG, 'queues', 'item_deleted', 'delete',
                   True, delete_item=tmp)
            return tmp

    def display(self):
        if not self.queue:
            tprint(LANG, 'queues', 'empty_queue', 'error', True)
        else:
            tprint(LANG, 'queues', 'queue_status', 'general', True)

            tprint(LANG, 'queues', 'queue_content', '',
                   False, indent=INDENT, content=self.queue)
