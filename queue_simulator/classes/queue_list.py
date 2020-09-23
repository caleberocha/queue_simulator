from .queue_sim import Queue
from ..decorators import singleton


@singleton
class QueueList:
    def __init__(self, queues):
        self.queues_params = queues
        self.reset_queues()

    def get_queue(self, index):
        return self.queues[index]

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
                q["capacity"],
                q["arrival"] if i == 0 else [None, None],
                q["service"],
            )
            for i, q in enumerate(self.queues_params)
        ]
        self.last_time = 0