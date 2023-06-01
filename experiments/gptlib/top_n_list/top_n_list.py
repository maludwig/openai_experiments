#!/usr/bin/env python
"""
extracts the concept of a top_n item list from the code below. I want it to be based on a given lambda function named "key", and a max_length integer n. The class should be called "TopNList" and should have an "addItem" function that takes in a new item to possibly add to the list, if the item happens to be in the top "n" based on the "key" function. The code I have currently works, but I want to make it generic. I also want an "addItems" and "asSortedList" function. Here is my current code:
"""
import heapq
from typing import Callable, Iterable, List, Tuple
from typing import TypeVar, Generic

T = TypeVar("T")


class TopNList(Generic[T]):
    """
    A class that maintains a list of the top N items based on a given key function.
    """

    def __init__(self, key: Callable[[T], float], max_length: int):
        """
        Initialize the TopNList.
        :param key: A lambda function that determines the "score" or "key" for a given item.
        :param max_length: The maximum number of items to keep in the top list.
        """
        self.key = key
        self.max_length = max_length
        self._heap = []

    def addItem(self, item: T) -> None:
        """
        Add an item to the top N list if it is in the top N based on the key function.
        :param item: The item to potentially add to the top list.
        """
        item_key = self.key(item)
        if len(self._heap) < self.max_length:
            heapq.heappush(self._heap, (item_key, item))
        else:
            heapq.heappushpop(self._heap, (item_key, item))

    def addItems(self, items: Iterable[T]) -> None:
        """
        Add multiple items to the top N list.
        :param items: An iterable of items to potentially add to the top list.
        """
        for item in items:
            self.addItem(item)

    def asSortedList(self) -> List[Tuple[float, T]]:
        """
        Return the top N list as a sorted list.
        :return: The sorted list representation of the top N items.
        """
        sorted_list = sorted(self._heap, key=lambda x: -x[0])
        return [(key, item) for key, item in sorted_list]


def main():
    """
    The main function for the TopNList.
    This is called when the script is run directly.
    """
    # Example usage of TopNList
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    key = lambda x: -abs(x - 5)
    max_length = 3

    top_n_list = TopNList(key, max_length)
    top_n_list.addItems(items)

    sorted_list = top_n_list.asSortedList()
    print(sorted_list)


if __name__ == "__main__":
    main()
