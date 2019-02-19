import pandas as pd
import math, os, sys, glob, re
import numpy as np
import warnings, logging, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from action_logging import Logger

warnings.filterwarnings('ignore')

class User:

    def __init__(self, user_name = None, messages = None, timestamp = None, logger = None):
        if logger is None:
            self.logger = Logger(log_flag = True, log_file = "user", log_path = "../logs/")
        else:
            self.logger = logger
        self.user_name = user_name
        self.logger.write_logger('In user.py (__init__): Initializing data for user: ' + self.user_name + ' starts')
        self.timestamp = timestamp
        self.messages = messages
        self.clean_messages = [] #Removed the following: emoji/media/links

        if self.user_name:
            self.data = pd.DataFrame({"Timestamp": timestamp, 'Messages': messages})

        self.words = []
        self.clean_words = []

        self.n_messages = 0
        self.n_words = 0
        self.n_unique_words = 0
        self.n_links = 0
        self.n_emoji = 0

        self.n_emoji_per_msg = []
        self.n_words_per_msg = []
        self.n_links_per_msg = []

        self.most_used_word = {"Word": "", "Count": 0}
        self.most_active_day = {"Date": None, "N_Messages": 0}

        self.avg_response_time = 0
        self.avg_messages_per_day = 0
        self.avg_words_per_message = 0
        self.avg_letters_per_word = 0

        self.longest_conversation_day = {'Date': None, 'N_Messages': 0, 'Duration': 0, 'N Words': 0, 'N Emojis': 0} # more time
        self.top_active_day = {'Date': None, 'N_Messages': 0, 'Duration': 0, 'N Words': 0, 'N Emojis': 0} # more messages
        self.top_20_words = {"Small": {"Words": [], "Count": []}, "Big": {"Words": [], "Count": []}}
        self.weekly_texts = {"Weekdays": [], "Count": []}

        self.n_words_per_day = None
        self.n_messages_per_day = None
        self.n_emoji_per_day = None

        self.first_msg_date = None
        self.recent_msg_date = None
        self.most_active_date = None
        self.least_active_date = None
        self.logger.write_logger('In user.py (__init__): Initializing data for user: ' + self.user_name + ' ends')

    def remove_emoticons(self, text):
        """
        Removes emoticons from text
        :return:
        """
        emoji_pattern = re.compile("["
                                   "\U0001F600-\U0001F64F"  # emoticons
                                   "\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   "\U0001F680-\U0001F6FF"  # transport & map symbols
                                   "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
        emoticons_ct = len(re.findall(emoji_pattern, text))
        text = emoji_pattern.sub(r'', text).strip()
        return text, emoticons_ct

    def remove_links(self, text):
        """
        Remove http/https links from message
        :param text:
        :return:
        """
        links_pattern = re.compile(r"http\S+", flags = re.UNICODE)
        links_ct = len(re.findall(links_pattern, text))
        text = links_pattern.sub(r'', text).strip()
        return text, links_ct

    def get_clean_messages(self):
        """
        Clean the messages
        - Remove Emojis
        - Remove URLs
        - Remove media
        :return:
        """
        self.logger.write_logger('In user.py (get_clean_messages): Cleaning of messages starts')

        self.clean_messages = [message for message in self.messages if "<Media omitted>" not in message]

        self.logger.write_logger('In user.py (remove_emoticons): Removing emoticons starts')
        self.clean_messages = [self.remove_emoticons(message)[0] for message in self.messages]
        self.logger.write_logger('In user.py (remove_emoticons): Removing emoticons ends')

        self.logger.write_logger('In user.py (remove_links): Removing links starts')
        self.clean_messages = [self.remove_links(message)[0] for message in self.messages]
        self.logger.write_logger('In user.py (remove_links): Removing links ends')

        self.logger.write_logger('In user.py (get_clean_messages): Cleaning of messages ends')

    def get_emoji_count(self):
        self.logger.write_logger('In user.py (get_emoji_count): Counting of emoji starts')
        self.n_emoji_per_msg = [self.remove_emoticons(message)[1] for message in self.messages]
        self.n_emoji = sum(self.n_emoji_per_msg)
        self.logger.write_logger('In user.py (get_emoji_count): Found ' + str(self.n_emoji) + ' emojis for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_emoji_count): Counting of emoji ends')

    def get_link_count(self):
        self.logger.write_logger('In user.py (get_link_count): Counting of links starts')
        self.n_links_per_msg = [self.remove_links(message)[1] for message in self.messages]
        self.n_links = sum(self.n_links_per_msg)
        self.logger.write_logger('In user.py (get_link_count): Found ' + str(self.n_links) + ' links for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_link_count): Counting of links ends')

    def get_message_count(self):
        self.logger.write_logger('In user.py (get_message_count): Counting of messages starts')
        self.n_messages = len(self.messages)
        self.logger.write_logger('In user.py (get_message_count): Found ' + str(self.n_messages) + ' Messages for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_message_count): Counting of messages ends')

    def get_word_count(self):
        self.logger.write_logger('In user.py (get_word_count): Counting of words starts')
        self.n_words_per_msg = [len(message.split()) for message in self.clean_messages]
        self.n_words = sum(self.n_words_per_msg)
        self.words = " ".join(self.messages).split(" ")
        self.logger.write_logger('In user.py (get_word_count): Found ' + str(self.n_words) + ' Words for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_word_count): Counting of words ends')

    def get_unique_words_count(self):
        self.logger.write_logger('In user.py (get_unique_words_count): Counting of unique words starts')
        self.unique_words = list(set(self.words))
        self.n_unique_words = len(self.unique_words)
        self.logger.write_logger('In user.py (get_unique_words_count): Found ' + str(self.n_unique_words) + ' Unique words for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_unique_words_count): Counting of unique words ends')

    def get_most_used_word(self):
        self.logger.write_logger('In user.py (get_most_used_word): Getting of most used word starts')
        self.clean_words = " ".join(self.clean_messages).split(" ")
        self.word_frequency = pd.DataFrame({"Words": self.clean_words, "Index": np.arange(self.n_words)})
        self.word_frequency = self.word_frequency.groupby("Words")['Index'].count().reset_index()
        self.word_frequency.rename(columns = {"Index": "Count"}, inplace = True)
        self.word_frequency = self.word_frequency.sort_values("Count", ascending = False)
        self.most_used_word = None
        self.logger.write_logger('In user.py (get_most_used_word): Most used word is: ' + str(self.most_used_word) + ' for: ' + self.user_name)
        self.logger.write_logger('In user.py (get_most_used_word): Getting of most used word ends')

    def get_interesting_dates(self, which = 'first'):
        self.logger.write_logger('In user.py (get_interesting_dates): Getting ' + which + ' date starts')
        if which == 'first':
            self.first_msg_date = min(self.timestamp)
        if which == 'recent':
            self.recent_msg_date = max(self.timestamp)
        self.logger.write_logger('In user.py (get_interesting_dates): Getting ' + which + ' date ends')