from functools import reduce
from ..errors import QueueFullError, SimCountNotDefinedError
from ..logger import logger


class Queue:
    def __init__(self, name, servers, capacity, arrival, service):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival, self.max_arrival = arrival
        self.min_service, self.max_service = service
        self.size = 0
        self.stats = {n: 0 for n in range(capacity + 1)}
        self.total_time = 0
        self.losses = 0
        self.serviced = 0
        self.logger = logger()

    def put(self, time):
        if self.capacity > 0 and self.size > self.capacity:
            raise QueueFullError()

        self.size += 1
        # self.logger.debug(f"Inserido em {repr(self)}")

    def get(self, time):
        self.size -= 1
        self.serviced += 1
        # self.logger.debug(f"Removido de {repr(self)}")

    def put_loss(self):
        self.losses += 1
        # self.logger.debug(f"Fila cheia - {repr(self)}")

    def update_times(self, last_time, prev_time):
        try:
            self.stats[self.size] += last_time - prev_time
        except KeyError:
            self.stats[self.size] = last_time - prev_time
        self.total_time += last_time - prev_time

    def avg_population(self, stats, total_time):
        return sum([n * (t / total_time) for n, t in stats.items()])

    def throughtput(self):
        return self.serviced / self.total_time

    def utilization(self, stats, total_time):
        return sum(
            [
                (t / total_time) * (min(n, self.servers) / self.servers)
                for n, t in stats.items()
            ]
        )

    def avg_wait_time(self, stats, total_time):
        return self.avg_population(stats, total_time) / self.throughtput()

    def show_stats(self, stats, total_time, losses):
        size_col1 = 10
        size_col2 = 20
        size_col3 = 17

        time_decimals = 4
        time_size = (
            len(
                "{:.{time_decimals}f}".format(
                    reduce(lambda a, b: max(int(a), int(b)), stats.values()),
                    time_decimals=time_decimals,
                )
            )
            + time_decimals
            + 1
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
        for n, time in stats.items():
            prob = "{:{prob_size}.{prob_decimals}f}%".format(
                time / total_time * 100,
                prob_size=prob_size - 1,
                prob_decimals=prob_decimals,
            )
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
        s += f"Perdas: {losses}\n"
        s += "População média: {:.4f}\n".format(self.avg_population(stats, total_time))
        s += "Vazão: {:.4f}\n".format(self.throughtput())
        s += "Utilização: {:.4f}\n".format(self.utilization(stats, total_time))
        s += "Tempo médio de espera: {:.4f}\n".format(self.avg_wait_time(stats, total_time))

        return s

    def __str__(self):
        return self.show_stats(self.stats, self.total_time, self.losses)

    def __repr__(self):
        return f"""Fila {self.name}: {[(n, time) for n, time in self.stats.items()]}, {self.losses} perdas"""


class SimResultQueue(Queue):
    def __init__(self, name, servers, capacity, arrival, service):
        super().__init__(name, servers, capacity, arrival, service)
        self.sim_count = 0

    def set_count(self, count):
        self.sim_count = count

    def __str__(self):
        if self.sim_count <= 0:
            raise SimCountNotDefinedError("Número de simulações não definido")
        
        
        return self.show_stats(
            {n: s / self.sim_count for n, s in self.stats.items()},
            self.total_time / self.sim_count,
            self.losses / self.sim_count,
        )
