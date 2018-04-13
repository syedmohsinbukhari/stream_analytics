# simulate that streamanalytics is installed as a python package
import context

import streamanalytics as sa
import logging

def setup_logging(log_fname):
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("{0}".format(log_fname))
    fileFormatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)s " +
                                      "- %(funcName)s() ] [%(levelname)s] " +
                                      "%(message)s")
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logging.INFO)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleFormatter = logging.Formatter("[%(levelname)s]  %(message)s")
    consoleHandler.setFormatter(consoleFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

def main():
    setup_logging("scripts/logs/extend_tweets.log")

    logging.info("Starting script extend_tweets.py")

    credentials = sa.utils.file_lines_to_array('scripts/conf/api_keys.txt')

    extender = sa.Extender(credentials)
    # extender('data/data.txt', 'data/data_extended.txt', num_tweets=100)
    extender.rate_limit_status('resources', 'statuses', '/statuses/lookup')

if __name__ == '__main__':
    main()
