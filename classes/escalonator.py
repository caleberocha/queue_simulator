from queue import PriorityQueue
from decorators import singleton
from errors import EmptyEscalonatorError
from logger import logger


@singleton
class Escalonator:
    def __init__(self):
        self.logger = logger()
        self.reset()

    def reset(self):
        self.queue = PriorityQueue(0)

    def put(self, event):
        self.queue.put((event.time, event))
        self.logger.debug(f"Evento inserido no escalonador: {event}")

    def get(self):
        try:
            event = self.queue.get(block=False)
            self.logger.debug(f"Evento removido do escalonador: {event}")
            return event
        except:
            raise EmptyEscalonatorError()