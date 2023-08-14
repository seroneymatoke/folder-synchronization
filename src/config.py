# Created by seroney
# Date: 12/08/2023
# Time: 12:04
# Purpose: Parse config arguments
# Implementation:
# TestData:

import os
import json
import argparse


def validate_config(config):
    """
    Validate the provided configuration dictionary.

    Args:
    - config (dict): Configuration dictionary.

    Returns:
    - bool: True if configuration is valid, False otherwise.
    """
    # Check source and replica folders
    if not os.path.isdir(config.get('source_folder', '')):
        raise ValueError("The provided source folder is not valid.")
    if not os.path.isdir(config.get('replica_folder', '')):
        raise ValueError("The provided replica folder is not valid.")

    # Check log path
    log_dir = os.path.dirname(config.get('log_path', ''))
    if log_dir and not os.path.exists(log_dir):
        raise ValueError("The directory for the log file does not exist.")

    # Check synchronization interval
    sync_interval = config.get('sync_interval', 0)
    if not isinstance(sync_interval, int) or sync_interval <= 0:
        raise ValueError("The synchronization interval must be a positive integer.")

    # Check max workers
    max_workers = config.get('max_workers', 0)
    if not isinstance(max_workers, int) or max_workers <= 0:
        raise ValueError("max_workers must be a positive integer.")

    # Check logging level
    allowed_logging_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if config.get('logging_level') not in allowed_logging_levels:
        raise ValueError(f"Logging level should be one of {allowed_logging_levels}.")

    return True


def load_config():
    """
    Load configuration from the command-line arguments, and, if not provided, fallback to config file values.

    Returns:
    - dict: Configuration dictionary.
    """
    parser = argparse.ArgumentParser(description="Synchronize folders.")
    parser.add_argument('--config', help="Path to configuration file.", default="config.json")
    parser.add_argument('--source_folder', help="Path to source folder.")
    parser.add_argument('--replica_folder', help="Path to replica folder.")
    parser.add_argument('--log_path', help="Path to log file.")
    parser.add_argument('--sync_interval', type=int, help="Synchronization interval in seconds.")
    parser.add_argument('--max_workers', type=int, help="Maximum number of workers for parallel execution.")
    parser.add_argument('--logging_level', help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

    args = parser.parse_args()

    # If config file is provided, load it as a default config
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Override with command line arguments, if provided
    if args.source_folder:
        config['source_folder'] = args.source_folder
    if args.replica_folder:
        config['replica_folder'] = args.replica_folder
    if args.log_path:
        config['log_path'] = args.log_path
    if args.sync_interval:
        config['sync_interval'] = args.sync_interval
    if args.max_workers:
        config['max_workers'] = args.max_workers
    if args.logging_level:
        config['logging_level'] = args.logging_level

    return config
