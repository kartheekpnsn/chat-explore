import pandas as pd
import math, os, sys, glob
import numpy as np
import warnings, logging, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class Logger:

    def __init__(self, log_flag = True, log_file = ""):
        self.log_flag = log_flag
        if self.log_flag:
            if log_file == "":
                self.log_file = 'chat-explore-log'
            else:
                self.log_file = log_file
            self.init_logger()

    def init_logger(self):
        """
        Initiates the logging object
        :return: None
        """
        os.makedirs('logs', exist_ok = True)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        logging.basicConfig(
            filename = 'logs/' + timestamp + '_' + self.log_file + '.log',
            format = '[%(asctime)s]:(# %(lineno)d) - %(levelname)s: %(message)s',
            level = logging.DEBUG)
        self.write_logger('Initiated the logger')

    def write_logger(self, message = "", error = False):
        """
        To write the logs and print them on console simultaneously
        :param message: string, message that needs to be printed in the logs
        :param error: bool, tells us whether the message is an error message
        :return: None
        """
        if error:
            if self.log_flag:
                logging.error(message)
            print('>> ERROR: ' + message + ' <<')
        else:
            if self.log_flag:
                logging.info(message)
            print('>> ' + message + ' <<')
