if __name__ == "__main__":
    import os, sys

    sys.path.append(os.path.join(sys.path[0], ".."))

from errors import NoMoreRandomNumbersError


class RandomGenerator:
    def __init__(self, seed, count):
        self.a = 25214903917
        self.c = 11
        self.m = 281474976710656
        self.x = seed
        self.count = count

    def next(self):
        if self.count <= 0:
            raise NoMoreRandomNumbersError()

        self.x = (self.a * self.x + self.c) % self.m
        self.count -= 1
        return self.x / self.m

    def size(self):
        return self.count


if __name__ == "__main__":
    rnd = RandomGenerator(12343, 100)
    while True:
        try:
            print(rnd.next())
        except NoMoreRandomNumbersError:
            print("fim")
            quit()