from .rnd_generator import RandomGenerator
from .rnd_numbers_list import RandomNumberList
from queue import Queue
from ..decorators import singleton
from ..logger import logger


@singleton
class RandomNumbers:
    def __init__(self):
        self.logger = logger()
        
    def set_source(self, seed=None, numbers_count=None, numbers=None):
        if seed is not None and numbers_count is not None:
            self.numbers = RandomGenerator(seed, numbers_count)
        elif numbers is not None:
            self.numbers = RandomNumberList(numbers)
        else:
            raise AttributeError("Nenhuma fonte de números aleatórios definida")

    def next(self):
        n = self.numbers.next()
        self.logger.debug(f"Random obtido: {n}")
        return n

    def size(self):
        return self.numbers.size()

    def empty(self):
        return self.size() == 0
