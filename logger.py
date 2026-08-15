import logging
from datetime import datetime


def create_scan_id():
    """
    Create a unique scan session identifier.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    return f"SR-{timestamp}"


def setup_logger(log_file=None):
    """
    Configure file-only logging.

    Logging is intentionally kept out of the
    normal terminal UI.
    """

    logger = logging.getLogger("synrecon")

    logger.setLevel(logging.INFO)

    logger.propagate = False

    # Remove existing handlers so repeated
    # setup calls do not duplicate messages.
    logger.handlers.clear()

    if log_file:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

    else:

        # No log file requested.
        # Keep logging silent.
        logger.addHandler(
            logging.NullHandler()
        )

    return logger
