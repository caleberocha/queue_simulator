from .queue_list import QueueList
from ..decorators import singleton


@singleton
class ElapsedTime:
    def __init__(self):
        # self.times = []
        self.last_time = 0
        self.prev_time = 0
        self.acc_time = 0

    def set(self, time):
        self.prev_time = self.last_time
        self.last_time = time
        # self.times.append(time)
        queue_list = QueueList()
        queue_list.update_times(self.last_time, self.prev_time)
        # print(f"Tempos: {self.times}")

    def reset(self):
        self.acc_time += self.last_time
        self.last_time = 0
        self.prev_time = 0

    # @property
    # def last_time(self):
    #     try:
    #         return self.times[-1]
    #     except:
    #         return 0

    # @property
    # def prev_time(self):
    #     try:
    #         return self.times[-2]
    #     except:
    #         return 0
