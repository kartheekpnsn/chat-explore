import logging
import datetime
import os
import sys

class Logger:
    def __init__(self, log_flag=True, log_file="", log_path=""):
        self.log_flag = log_flag
        self.log_path = log_path
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        if self.log_flag:
            if log_file == "":
                print('Please provide the log file name')
                sys.exit()
            else:
                self.log_file = log_file
                self.filename = self.log_path + timestamp + '-' + self.log_file + '.log'
            self.format = '[%(asctime)s]:(# %(lineno)d) - %(levelname)s: %(message)s'
            self.init_logger()

    def init_logger(self):
        """
        Initiates the logging object
        :return: None
        """
        os.makedirs(self.log_path, exist_ok=True)
        formatter = logging.Formatter(self.format)
        handler = logging.FileHandler(self.filename, 'w', 'utf-8')
        handler.setFormatter(formatter)

        logger = logging.getLogger(self.log_file)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        self.logger = logger

    def write_logger(self, message="", error=False):
        """
        To write the logs and print them on console simultaneously
        :param message: string, message that needs to be printed in the logs
        :param error: bool, tells us whether the message is an error message
        :return: None
        """
        if error:
            if self.log_flag:
                self.logger.error(message)
            print('>> ERROR: ' + message + ' <<')
        else:
            if self.log_flag:
                self.logger.info(message)
            print('>> ' + message + ' <<')