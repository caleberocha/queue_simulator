from .rnd_generator import RandomGenerator
from .rnd_numbers_list import RandomNumberList
from queue import Queue
from ..decorators import singleton


@singleton
class RandomNumbers:
    def set_source(self, seed=None, numbers_count=None, numbers=None):
        if seed is not None and numbers_count is not None:
            self.numbers = RandomGenerator(seed, numbers_count)
        elif numbers is not None:
            self.numbers = RandomNumberList(numbers)
        else:
            raise AttributeError("Nenhuma fonte de números aleatórios definida")

    def next(self):
        return self.numbers.next()

    def size(self):
        return self.numbers.size()

    def empty(self):
        return self.size() == 0
