# Created by seroney
# Date: 13/08/2023
# Time: 12:54
# Purpose: 
# Implementation:
# TestData:
import argparse
import logging
import time
from synchronizer import sync_folders
from logger import setup_logging


def main():
    parser = argparse.ArgumentParser(description='Synchronize source folder to replica folder.')

    parser.add_argument('--source', type=str, required=True, help='Path to the source folder.')
    parser.add_argument('--replica', type=str, required=True, help='Path to the replica folder.')
    parser.add_argument('--log_file', type=str, default='sync.log', help='Path to the log file.')
    parser.add_argument('--log_level', type=str, default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Logging level.')
    parser.add_argument('--max_workers', type=int, default=None,
                        help='Maximum number of worker threads for parallelism.')
    parser.add_argument('--interval', type=int, default=60,
                        help='Time interval (in seconds) for periodic synchronization.')

    args = parser.parse_args()

    setup_logging(args.log_file, args.log_level)

    while True:
        try:
            logging.info("Starting synchronization...")
            sync_folders(args.source, args.replica, args.max_workers)
            logging.info("Synchronization complete. Waiting for the next cycle...")
            time.sleep(args.interval)
        except Exception as e:
            logging.error(f"An error occurred during synchronization: {e}")
            break


if __name__ == '__main__':
    main()
