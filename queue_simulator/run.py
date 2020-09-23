import json
import logging
from .classes.event import Event
from .classes.queue_list import QueueList
from .classes.escalonator import Escalonator
from .classes.rnd_numbers import RandomNumbers
from .classes.sim_result import SimulationResult
from .classes.elapsed_time import ElapsedTime
from .functions import parse_args
from .errors import NoInputError, NoMoreRandomNumbersError, UnexpectedError
from .logger import logger


def run_simulator(input_file=None, input_json=None, log_level=logging.INFO):
    log = logger(log_level)
    results = []

    if input_file is not None:
        with open(input_file, "r") as f:
            params = json.load(f)
    elif input_json is not None:
        try:
            params = json.loads(input_json)
        except json.JSONDecodeError:
            log.error("JSON inválido")
            return 1
    else:
        raise NoInputError()

    try:
        initial_event = params["initialEvent"]
        queues = QueueList(params["queues"])
        try:
            seeds = params["seeds"]
            random_count = params["random_count"]
            simulations = len(seeds)
        except KeyError:
            seeds = None
            simulations = 1
            rnd_numbers_list = params["rndNumbers"]
    except KeyError as e:
        log.error(f"Elemento {e} não encontrado")
        return 2
    except ValueError:
        log.error(f""""arrival" (apenas fila 1) e "service" devem ser listas com 2 elementos""")
        return 3

    escalonator = Escalonator()
    elapsed_time = ElapsedTime()
    rnd_numbers = RandomNumbers()
    sim_result = SimulationResult()

    for i in range(simulations):
        log.info(f"Executando simulação {i+1}")
        escalonator.reset()
        escalonator.put(Event(initial_event["time"], -1, 0))
        queues.reset_queues()
        elapsed_time.reset()

        if seeds is None:
            log.info("Utilizando lista de números")
            rnd_numbers.set_source(numbers=rnd_numbers_list)
        else:
            seed = seeds[i]
            log.info(f"Utilizando semente {seed}")
            rnd_numbers.set_source(seed=seed, numbers_count=random_count)

        while not rnd_numbers.empty():
            try:
                time, event = escalonator.get()
                event.run()
            except NoMoreRandomNumbersError:
                log.warning("Não há mais números aleatórios")
            except UnexpectedError as e:
                log.error(str(e))
                return 4

        sim_result.collect()

    elapsed_time.reset()
    log.info(sim_result.get_result())
    return 0


if __name__ == "__main__":
    try:
        args = parse_args()
    except AttributeError as e:
        print(f"Erro: {e}")
        quit(1)

    retval = run_simulator(**args)
    quit(retval)
