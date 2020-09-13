from queue import Queue, Empty
from errors import NoMoreRandomNumbersError


class RandomNumberList:
    def __init__(self, numbers):
        self.numbers = Queue()
        for number in numbers:
            self.numbers.put(number)

    def next(self):
        try:
            return self.numbers.get(block=False)
        except Empty:
            raise NoMoreRandomNumbersError()

    def size(self):
        return self.numbers.qsize()
