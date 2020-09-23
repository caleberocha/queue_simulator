from .queue_list import QueueList
from .escalonator import Escalonator
from .rnd_numbers import RandomNumbers
from .elapsed_time import ElapsedTime
from ..functions import conversion
from ..errors import UnexpectedError


class Event:
    def __init__(self, time, queue_index=-1, next_queue_index=-1):
        self.time = time
        self.queue_index = queue_index
        self.next_queue_index = next_queue_index

    def __str__(self):
        return f"Evento ({self.time}, {self.queue_index}, {self.next_queue_index})"

    def __repr__(self):
        return str(self)

    def run(self):
        queue_list = QueueList()
        escalonator = Escalonator()
        rnd_numbers = RandomNumbers()
        elapsed_time = ElapsedTime()

        elapsed_time.set(self.time)

        if self.queue_index >= 0:
            queue = queue_list.get_queue(self.queue_index)
            queue.get(self.time)

            if queue.size >= queue.servers:
                new_time = conversion(
                    queue.min_service,
                    queue.max_service,
                    rnd_numbers.next(),
                )
                event = Event(
                    new_time + elapsed_time.last_time,
                    self.queue_index,
                    self.next_queue_index,
                )

                escalonator.put(event)

        if self.next_queue_index >= 0 and self.next_queue_index < queue_list.size():
            next_queue = queue_list.get_queue(self.next_queue_index)
            if next_queue.size >= next_queue.capacity:
                next_queue.put_loss()
            else:
                next_queue.put(self.time)
                if next_queue.size <= next_queue.servers:
                    new_time = conversion(
                        next_queue.min_service,
                        next_queue.max_service,
                        rnd_numbers.next(),
                    )
                    event = Event(
                        new_time + elapsed_time.last_time,
                        self.next_queue_index,
                        self.next_queue_index + 1,
                    )
                    escalonator.put(event)

            if self.queue_index == -1:
                if next_queue.min_arrival is None or next_queue.max_arrival is None:
                    raise UnexpectedError(f"Fila {next_queue.name} sem arrival definido, isso não deveria acontecer!")

                new_time = conversion(
                    next_queue.min_arrival,
                    next_queue.max_arrival,
                    rnd_numbers.next(),
                )
                event = Event(
                    new_time + elapsed_time.last_time,
                    self.queue_index,
                    self.next_queue_index,
                )
                escalonator.put(event)
