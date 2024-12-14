import asyncio
import random
from collections.abc import Sequence
from typing import Any


# TODO(ThomasHepworth): Perhaps we should turn this into an ordered set instead of a list.
# Then, we can pop elements by name, and we can also check if an element is in the queue.
class SongQueue(asyncio.Queue, Sequence):
    """
    A song queue that extends asyncio.Queue and behaves like a list for easy manipulation.
    """

    def __getitem__(self, index: int | slice):
        items = self._get_items_snapshot()
        if isinstance(index, slice):
            return items[index]
        return items[index]

    def __len__(self):
        return self.qsize()

    def __iter__(self):
        return iter(self._get_items_snapshot())

    def clear(self):
        while not self.empty():
            self.get_nowait()

    def shuffle(self):
        items = self._get_items_snapshot()
        random.shuffle(items)
        self._rebuild_queue(items)

    def remove(self, index: int):
        items = self._get_items_snapshot()
        if 0 <= index < len(items):
            del items[index]
            self._rebuild_queue(items)
        else:
            raise IndexError("Index out of range")

    def peek(self) -> Any:
        if self.empty():
            raise asyncio.QueueEmpty("Queue is empty")
        return self._get_items_snapshot()[0]

    def as_list(self) -> list:
        return self._get_items_snapshot()

    def _get_items_snapshot(self) -> list:
        return list(self._queue)

    def _rebuild_queue(self, items: list):
        self._queue.clear()
        for item in items:
            self.put_nowait(item)
