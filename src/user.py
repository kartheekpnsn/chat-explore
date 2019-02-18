import pandas as pd
import math, os, sys, glob, re
import numpy as np
import warnings, logging, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

class User:

    def __init__(self, user_name = None, messages = None, timestamp = None):
        self.user_name = user_name
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

        self.longest_conversation_day = {'Date': None, 'N_Messages': 0, 'Duration': 0}
        self.top_20_words = {"Small": {"Words": [], "Count": []}, "Big": {"Words": [], "Count": []}}
        self.weekly_texts = {"Weekdays": [], "Count": []}

        self.n_words_per_day = None
        self.n_messages_per_day = None
        self.n_emoji_per_day = None

    def remove_emoticons(self, text):
        """
        Removes emoticons from text
        :return:
        """
        # self.logger.write_logger('Removing emoticons from: "' + text + '" starts')
        emoji_pattern = re.compile("["
                                   "\U0001F600-\U0001F64F"  # emoticons
                                   "\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   "\U0001F680-\U0001F6FF"  # transport & map symbols
                                   "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
        emoticons_ct = len(re.findall(emoji_pattern, text))
        text = emoji_pattern.sub(r'', text).strip()
        # self.logger.write_logger('Removing emoticons from: "' + text + '" ends')
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
        self.clean_messages = [message for message in self.messages if "<Media omitted>" not in message]
        self.clean_messages = [self.remove_emoticons(message)[0] for message in self.messages]
        self.clean_messages = [self.remove_links(message)[0] for message in self.messages]

    def get_emoji_count(self):
        self.n_emoji_per_msg = [self.remove_emoticons(message)[1] for message in self.messages]
        self.n_emoji = sum(self.n_emoji_per_msg)

    def get_link_count(self):
        self.n_links_per_msg = [self.remove_links(message)[1] for message in self.messages]
        self.n_links = sum(self.n_links_per_msg)

    def get_message_count(self):
        self.n_messages = len(self.messages)

    def get_word_count(self):
        self.n_words_per_msg = [len(message.split()) for message in self.clean_messages]
        self.n_words = sum(self.n_words_per_msg)
        self.words = " ".join(self.messages).split(" ")

    def get_unique_words_count(self):
        self.unique_words = list(set(self.words))
        self.n_unique_words = len(self.unique_words)

    def get_most_used_word(self):
        self.clean_words = " ".join(self.clean_messages).split(" ")
        self.word_frequency = pd.DataFrame({"Words": self.clean_words, "Index": np.arange(self.n_words)})
        self.word_frequency = self.word_frequency.groupby("Words")['Index'].count().reset_index()
        self.word_frequency.rename(columns = {"Index": "Count"}, inplace = True)
        self.word_frequency = self.word_frequency.sort_values("Count", ascending = False)
        self.most_used_word = None


user = User(None, None, None)
print(user.remove_links(text = 'Hello world https://www.google.com'))