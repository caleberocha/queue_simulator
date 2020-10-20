from .queue_sim import Queue
from ..decorators import singleton
from ..errors import QueueNotFoundError


@singleton
class QueueList:
    def __init__(self, queues):
        self.queues_params = queues
        self.reset_queues()

    def get_queue(self, index):
        return self.queues[index]

    def get_queue_by_name(self, name):
        try:
            return [q for q in self.queues if q.name == name][0]
        except IndexError:
            raise QueueNotFoundError(f"Fila {name} não encontrada")

    def get_queue_index_by_name(self, name):
        for i, q in enumerate(self.queues):
            if q.name == name:
                return i

        raise QueueNotFoundError(f"Fila {name} não encontrada")

    def size(self):
        return len(self.queues)

    def update_times(self, last_time, prev_time):
        for q in self.queues:
            q.update_times(last_time, prev_time)

    def reset_queues(self):
        self.queues = [
            Queue(
                q["name"],
                q["servers"],
                q["capacity"] if "capacity" in q else 0,
                q["arrival"] if i == 0 else [None, None],
                q["service"],
            )
            for i, q in enumerate(self.queues_params)
        ]
        self.last_time = 0