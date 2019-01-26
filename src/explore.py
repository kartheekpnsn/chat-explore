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


class Preprocess:

    def __init__(self, input_file):
        """
        Initialize Preprocess class
        :param input_file:
        """
        self.file = input_file
        self.logger = Logger(log_flag = False)
        self.data = None
        self.data_backup = None
        self.pd_data = None

    def read_file(self):
        """
        Reads in the file in UTF-8 encoding and splits into lines
        Also, takes backup just to have control on things.
        :return:
        """
        f = open(self.file, 'r', encoding = "utf8")
        self.data = f.read()
        f.close()
        self.data = self.data.splitlines()

        # Save temporary value
        self.data_backup = self.data.copy()

    def print_sample(self, n_lines = 10):
        """
        Prints sample number of lines
        :param n_lines:
        :return:
        """
        print(self.data[:n_lines])

    def add_missing_info(self, current_line, previous_line):
        """
        Add timestamp, username from previous line
        :param current_line:
        :param previous_line:
        :return:
        """
        previous_line_ts = previous_line.split('-')[0].strip()
        previous_line_name = previous_line.split('-')[1].strip().split(':')[0].strip()
        current_line = previous_line_ts + " - " + previous_line_name + ": " + current_line
        return current_line

    def clean_data(self):
        """
        Cleans data by adding missing information
        :return:
        """
        self.data = self.data_backup.copy()
        for idx, line in enumerate(self.data):
            split_part = line.split('-')
            if len(split_part) == 0:
                self.logger.write_logger(f'== Before Condition 1: {self.data[idx]}')
                self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                self.logger.write_logger(f'== After Condition 1: {self.data[idx-1]}')
                self.logger.write_logger(f'== After Condition 1: {self.data[idx]}')
            else:
                split_part = split_part[0].strip()
                split_part = split_part.split(",")
                if len(split_part) < 2:
                    self.logger.write_logger(f'== Before Condition 2: {self.data[idx]}')
                    self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                    self.logger.write_logger(f'== After Condition 2: {self.data[idx-1]}')
                    self.logger.write_logger(f'== After Condition 2: {self.data[idx]}')
                else:
                    split_part = split_part[1].strip()
                    split_part = split_part.split(" ")
                    if len(split_part) < 2:
                        self.logger.write_logger(f'== Before Condition 3: {self.data[idx]}')
                        self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                        self.logger.write_logger(f'== After Condition 3: {self.data[idx-1]}')
                        self.logger.write_logger(f'== After Condition 3: {self.data[idx]}')
                    else:
                        split_part = split_part[1].strip()
                        if split_part != 'am' and split_part != 'pm':
                            self.logger.write_logger(f'== Before Condition 4: {self.data[idx]}')
                            self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                            self.logger.write_logger(f'== After Condition 4: {self.data[idx-1]}')
                            self.logger.write_logger(f'== After Condition 4: {self.data[idx]}')
                        else:
                            'No correction needed'

    def drop_message(self, contains = 'Messages to this chat and calls are now secured with end-to-end encryption'):
        """
        Drops the message if it contains the text given in parameter
        :param contains:
        :return:
        """
        self.data = [line for line in self.data if contains not in line]

    def prepare_df(self):
        """
        Prepares a Pandas Dataframe out of the data
        :return:
        """
        timestamps = []
        users = []
        messages = []
        for line in self.data:
            timestamps.append(line.split("-")[0].strip())
            sub_line = line.split("-")[1].strip().split(":")
            users.append(sub_line[0].strip())
            messages.append("-".join([v.strip() for v in sub_line[1:]]))
        self.pd_data = pd.DataFrame({'Timestamp': timestamps, 'User': users, 'Message': messages})[
            ['Timestamp', 'User', 'Message']]
        self.pd_data['Timestamp'] = pd.to_datetime(self.pd_data['Timestamp'])
        self.pd_data['Date'] = self.pd_data['Timestamp'].dt.strftime('%d-%m-%Y')
        self.pd_data['Weekday'] = self.pd_data['Timestamp'].dt.strftime('%a')


class User:

    def __init__(self, user_name, messages, timestamp):
        self.user_name = user_name
        self.timestamp = timestamp
        self.messages = messages
        self.data = pd.DataFrame({"Timestamp": timestamp, 'Messages': messages})
        self.n_messages = 0
        self.n_words = 0
        self.n_unique_words = 0
        self.n_links = 0
        self.n_emoji = 0
        self.most_used_word = {"Word": "", "Count": 0}
        self.most_active_day = {"Date": None, "N_Messages": 0}
        self.avg_response_time = 0
        self.avg_messages_per_day = 0
        self.avg_words_per_message = 0
        self.avg_letters_per_word = 0
        self.longest_conversation_day = {'Date': None, 'N_Messages': 0, 'Duration': 0}
        self.top_20_words = {"Small": {"Words": [], "Count": []}, "Big": {"Words": [], "Count": []}}
        self.weekly_texts = {"Weekdays": [], "Count": []}
        self.n_words_per_day = None
        self.n_emoji_per_day = None

    def count_messages(self):
        self.n_messages = len(self.messages)


class Explore:

    def __init__(self, pd_data):
        self.pd_data = pd_data
