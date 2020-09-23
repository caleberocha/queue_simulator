import sys
import logging


def parse_args():
    input_file = None
    input_json = None
    log_level = logging.INFO

    i = 1
    try:
        arg = sys.argv[i]
    except IndexError:
        raise AttributeError("Não foi especificado arquivo ou string json")

    while True:
        try:
            if arg == "--debug":
                log_level = logging.DEBUG
            elif arg == "--json":
                i += 1
                try:
                    arg = sys.argv[i]
                    if arg.startswith("-"):
                        raise IndexError
                except IndexError:
                    raise AttributeError("Argumento inválido após --json")
                input_json = arg
            else:
                input_file = arg
            i += 1
            arg = sys.argv[i]
        except IndexError:
            break

    if input_file and input_json:
        input_json = None

    if not input_file and not input_json:
        raise AttributeError("Não foi especificado arquivo ou string json")

    return {"input_file": input_file, "input_json": input_json, "log_level": log_level}


def conversion(a, b, rnd_number):
    return (b - a) * rnd_number + a