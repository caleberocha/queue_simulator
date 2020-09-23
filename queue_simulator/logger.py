import logging


def logger(level=logging.INFO):
    return _setup_logger("queue_simulator", level)


def _setup_logger(name, level):
    logr = logging.getLogger(name)

    if [h for h in logr.handlers if h.get_name() == name]:
        return logr

    logr.setLevel(level)

    logc = logging.StreamHandler()
    logc.set_name(name)
    logc.setFormatter(LogFormat())
    logc.setLevel(level)
    logr.addHandler(logc)

    return logr


class LogFormat(logging.Formatter):
    err_fmt  = "ERRO: %(msg)s"
    dbg_fmt  = "DEBUG: %(msg)s"
    info_fmt = "%(msg)s"

    def __init__(self):
        super().__init__(fmt="%(msg)s")  
    
    def format(self, record):
        format_orig = self._style._fmt

        if record.levelno == logging.DEBUG:
            self._style._fmt = LogFormat.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = LogFormat.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = LogFormat.err_fmt

        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig

        return result