from functools import reduce
from errors import QueueFullError
from logger import logger


class Queue:
    def __init__(self, name, servers, capacity, arrival, service):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival, self.max_arrival = arrival
        self.min_service, self.max_service = service
        self.size = 0
        self.stats = [0 for n in range(capacity + 1)]
        self.total_time = 0
        self.losses = 0
        self.logger = logger()

    def put(self, time):
        if self.size > self.capacity:
            raise QueueFullError()

        self.size += 1
        self.logger.debug(f"Inserido em {repr(self)}")

    def get(self, time):
        self.size -= 1
        self.logger.debug(f"Removido de {repr(self)}")

    def put_loss(self):
        self.losses += 1
        self.logger.debug(f"Fila cheia - {repr(self)}")

    def update_times(self, last_time, prev_time):
        self.stats[self.size] += last_time - prev_time
        self.total_time += last_time - prev_time

    def __str__(self):
        size_col1 = 10
        size_col2 = 20
        size_col3 = 17

        time_decimals = 4
        time_size = (
            len(str(reduce(lambda a, b: max(int(a), int(b)), self.stats)))
            + time_decimals + 1
        )
        time_spaces_left = (size_col2 - time_size) // 2
        time_spaces_right = size_col2 - time_size - time_spaces_left

        prob_decimals = 2
        prob_size = 7
        prob_spaces_left = (size_col3 - prob_size) // 2
        prob_spaces_right = size_col3 - prob_size - prob_spaces_left

        s = f"Fila {self.name} (G/G/{self.servers}/{self.capacity})\n"
        s += "|{:^{size_col1}}|{:^{size_col2}}|{:^{size_col3}}|\n".format(
            "Estado",
            "Tempo",
            "Probabilidade",
            size_col1=size_col1,
            size_col2=size_col2,
            size_col3=size_col3,
        )
        s += "|{c1}|{c2}|{c3}|\n".format(
            c1="-" * size_col1,
            c2="-" * size_col2,
            c3="-" * size_col3,
        )
        for n, time in enumerate(self.stats):
            prob = "{:{prob_size}.{prob_decimals}f}%".format(time / self.total_time * 100, prob_size=prob_size - 1, prob_decimals=prob_decimals)
            s += "|{:^{size_col1}}|{:{time_spaces_left}}{:{time_size}.{time_decimals}f}{:{time_spaces_right}}|{:{prob_spaces_left}}{:{prob_size}}{:{prob_spaces_right}}|\n".format(
                n,
                " ",
                time,
                " ",
                " ",
                prob,
                " ",
                size_col1=size_col1,
                time_spaces_left=time_spaces_left,
                time_size=time_size,
                time_decimals=time_decimals,
                time_spaces_right=time_spaces_right,
                prob_spaces_left=prob_spaces_left,
                prob_size=prob_size,
                prob_spaces_right=prob_spaces_right,
            )
        s += f"Perdas: {self.losses}\n"

        return s

    def __repr__(self):
        return f"""Fila {self.name}: {[(n, time) for n, time in enumerate(self.stats)]}, {self.losses} perdas"""