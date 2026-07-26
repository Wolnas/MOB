import logging


def get_logger():

    logger = logging.getLogger("HospitalScraper")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console)

    return logger