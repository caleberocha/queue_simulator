from .run import parse_args, run_simulator


if __name__ == "__main__":
    try:
        args = parse_args()
    except AttributeError as e:
        print(f"Erro: {e}")
        quit(1)

    retval = run_simulator(**args)
    quit(retval)