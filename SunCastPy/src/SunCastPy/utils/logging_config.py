import logging
import sys


def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        if level == logging.DEBUG:
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        else:
            formatter = logging.Formatter("[%(levelname)s]\t%(message)s")

        handler.setFormatter(formatter)
        root.addHandler(handler)
