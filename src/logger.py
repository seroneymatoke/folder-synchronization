# Created by seroney
# Date: 14/08/2023
# Time: 2:48
# Purpose: Logger Utility
# Implementation:
# TestData:

import logging


def setup_logging(log_file, log_level):
    """
    Set up logging configuration.

    Args:
    - log_file (str): Path to the log file.
    - log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logging.basicConfig(filename=log_file, level=log_level.upper(),
                        format='%(asctime)s - %(levelname)s - %(message)s')
    console = logging.StreamHandler()
    console.setLevel(log_level.upper())
    formatter = logging.Formatter('%%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
