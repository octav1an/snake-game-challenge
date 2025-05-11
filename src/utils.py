import typing
from collections import deque
from contextlib import contextmanager


@contextmanager
def animation_off(screen):
    try:
        yield screen.tracer(0)
    finally:
        screen.update()


class Queue:
    def __init__(self):
        self.items_deck = deque()  # for fast appends and pops
        self.items_set = set()  # for fast lookups

    def append(self, item: typing.Any):
        """Append to the left"""
        self.items_deck.appendleft(item)
        self.items_set.add(item)

    def append_right(self, item: typing.Any):
        """Append to the right"""
        self.items_deck.append(item)
        self.items_set.add(item)

    def pop(self) -> typing.Any:
        """Pops the right item in the queue"""
        item = self.items_deck.pop()
        self.items_set.remove(item)
        return item

    def __contains__(self, key) -> bool:
        return key in self.items_set
