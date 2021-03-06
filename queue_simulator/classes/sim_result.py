from functools import reduce
from .queue_list import QueueList
from .queue_sim import Queue, SimResultQueue
from .elapsed_time import ElapsedTime


class SimulationResult:
    def __init__(self):
        self.results = []
        self.acc_result = []

    def collect(self):
        qlist = QueueList()
        self.results.append(qlist.queues)

        if len(self.acc_result) == 0:
            for q in qlist.queues:
                qc = SimResultQueue(
                    q.name,
                    q.servers,
                    q.capacity,
                    [q.min_arrival, q.max_arrival],
                    [q.min_service, q.max_service],
                )
                qc.stats = q.stats.copy()
                qc.total_time = q.total_time
                qc.losses = q.losses
                qc.serviced = q.serviced
                self.acc_result.append(qc)
        else:
            for i, q in enumerate(qlist.queues):
                for j in range(len(self.acc_result[i].stats)):
                    try:
                        self.acc_result[i].stats[j] += q.stats[j]
                    except KeyError:
                        pass
                self.acc_result[i].total_time += q.total_time
                self.acc_result[i].losses += q.losses
                self.acc_result[i].serviced += q.serviced

    def get_result(self):
        elapsed_time = ElapsedTime()
        for q in self.acc_result:
            q.set_count(len(self.results))
        return "\n".join(
            [str(q) for q in self.acc_result]
        ) + "\nTempo médio de simulação: {:.4f}\n".format(
            elapsed_time.acc_time / len(self.results)
        )

    def get_result_analytical(self):
        s = ""
        for i, r in enumerate(self.results):
            s += f"Simulação {i+1}\n"
            s += "\n".join([str(q) for q in r]) + "\n"
        return s