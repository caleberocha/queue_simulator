from .rnd_numbers import RandomNumbers
from ..decorators import singleton


@singleton
class Network:
    def __init__(self, network, queues):
        self.network = {}
        self.exit = queues.size()

        for n in network:
            source = queues.get_queue_index_by_name(n["source"])
            obj = {
                "target": queues.get_queue_index_by_name(n["target"]),
                "probability": float(n["probability"]),
            }
            try:
                self.network[source].append(obj)
            except KeyError:
                self.network[source] = [obj]

        for source in self.network.keys():
            self.network[source] = sorted(
                self.network[source], key=lambda q: q["probability"]
            )

        # Sem probabilidade de roteamento
        if len(self.network) == 0:
            self.network = {
                q: [{"target": q + 1, "probability": 1.0}] for q in range(queues.size())
            }

    def target_queue_index(self, queue_index):
        # Evento inicial
        if queue_index == -1:
            return 0

        try:
            targets = self.network[queue_index]

            # Sem probabilidade de roteamento
            if len(targets) == 1 and targets[0]["probability"] == 1.0:
                return targets[0]["target"]

            # Com probabilidade de roteamento
            rnd_numbers = RandomNumbers()
            rand = rnd_numbers.next()
            for q in targets:
                if rand < q["probability"]:
                    return q["target"]
                rand = rand - q["probability"]
            return self.exit
        except KeyError:
            return self.exit
