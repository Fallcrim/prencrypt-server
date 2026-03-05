import logging


def setup_logging(log_file=None, log_level=logging.INFO):
    """
    Sets up logging for the application. If log_file is provided, logs will be written to the specified file. Otherwise, logs will be printed to the console.
    :param log_file: Optional path to a log file. If None, logs will be printed to the console.
    :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG). Default is logging.INFO.
    """
    if log_file:
        logging.basicConfig(filename=log_file, level=log_level,
                            format='%(asctime)s - [%(levelname)s] %(name)s - %(message)s')
    else:
        logging.basicConfig(level=log_level,
                            format='%(asctime)s - [%(levelname)s] %(name)s - %(message)s')


setup_logging("prencrypt.log", logging.DEBUG)
