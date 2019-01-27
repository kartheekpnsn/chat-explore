import pandas as pd
import math, os, sys, glob
import numpy as np
import warnings, logging, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

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
