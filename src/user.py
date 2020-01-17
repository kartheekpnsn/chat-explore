import re
import string
import warnings

import numpy as np
import pandas as pd
import tldextract
import nltk

# this resolves SSL certificate issues for a MAC user
import ssl

# disable SSL check
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('wordnet')

# from nltk.corpus import stopwords # Removed it to fit requirements better
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams

from scipy import stats

from action_logging import Logger
from response import Response
from sentiment_analysis import Sentiment

warnings.filterwarnings('ignore')


class User:

    def __init__(self, user_name = None, color_map = None, messages = None, timestamp = None, users = None,
                 logger = None):

        if logger is None:
            self.logger = Logger(log_flag = True, log_file = "user", log_path = "../logs/")
        else:
            self.logger = logger

        if user_name is None:
            user_name = "None"
        self.user_name = user_name
        self.logger.write_logger(f'In user.py (__init__): Initializing members for user: {self.user_name} starts')

        # Color code for the user;
        if color_map is None:
            self.user_color = "#2ecc71"  # green
        else:
            if self.user_name in color_map.keys():
                self.user_color = color_map[self.user_name]
            else:
                self.user_color = "#2ecc71"  # green

        # Store the time stamp list for the user
        self.timestamp = timestamp
        # Store the message list for the user
        self.messages = messages
        # Store the user list for the overall data
        self.users = users
        # Pandas dataframe of messages and timestamps
        self.prepare_dataframe()

        self.clean_messages = []  # Removed the following: emoji/media/links
        self.words = []  # Words from the messages list
        self.pd_word_df = None
        self.bigrams = []  # Bigram Words from the messages list
        self.pd_bigrams_df = None
        self.trigrams = []  # Bigram Words from the messages list
        self.pd_trigrams_df = None
        self.clean_words = []  # Words from the clean messages list
        self.clean_bigrams = []  # Bigram Words from the clean messages list
        self.clean_trigrams = []  # Bigram Words from the clean messages list

        self.pd_emoji_df = None

        # Initialize the default values
        self._init_members()

        self.logger.write_logger('In user.py (__init__): Initializing members for user: ' + self.user_name + ' ends')

    def _init_totals(self):
        """

        :return:
        """
        self.n_messages = 0
        self.n_words = 0
        self.n_unique_words = 0
        self.n_links = 0
        self.n_emoji = 0
        self.n_screen_touches = 0

        self.most_used_word = {"Word": "", "Count": 0}
        self.most_used_double_word = {"Word": "", "Count": 0}
        self.most_used_triple_word = {"Word": "", "Count": 0}

        self.first_msg_date = {"Date": None, "N_Messages": 0}
        self.recent_msg_date = {"Date": None, "N_Messages": 0}
        self.most_active_date = {"Date": None, "N_Messages": 0}
        self.least_active_date = {"Date": None, "N_Messages": 0}

        self.most_used_emoji = {"Emoji": "", "Count": 0}

        self.avg_response_time = 0

        self.n_days = 0  # Get start date and recent date, calculate difference
        self.n_days_chatted = 0

    def _init_averages(self):
        """

        :return:
        """
        self.avg_messages_per_day = 0
        self.avg_emojis_per_day = 0
        self.avg_links_per_day = 0
        self.avg_words_per_message = 0
        self.avg_letters_per_message = 0

    def _init_tops(self):
        """

        :return:
        """
        self.longest_conversation_day = {
            'Date'          : None,
            'N_Messages'    : 0,
            'Duration (Min)': 0,
            'N Words'       : 0,
            'N Emojis'      : 0
        }  # more time
        self.top_active_day = {
            'Date'          : None,
            'N_Messages'    : 0,
            'Duration (Min)': 0,
            'N Words'       : 0,
            'N Emojis'      : 0
        }  # more messages

        self.top_k_positive_str = ""
        self.top_k_negative_str = ""

    def _init_plot_members(self):
        """

        :return:
        """
        self.top_20_words = {"Small": {"Words": [], "Count": []}, "Big": {"Words": [], "Count": []}}
        self.weekly_texts = {"Weekdays": [], "Count": []}

        self.n_words_per_day = None
        self.n_messages_per_day = None
        self.n_emoji_per_day = None

    def _init_members(self):
        """

        :return:
        """
        # INIT FOR TOTALS =================================================================
        self._init_totals()

        # INIT FOR AVERAGES ===============================================================
        self._init_averages()

        # INIT FOR TOPS ===================================================================
        self._init_tops()

        # INIT FOR PLOTS ==================================================================
        self._init_plot_members()

    def prepare_dataframe(self):
        """

        :return:
        """
        if self.user_name:
            self.data = pd.DataFrame({"TimeStamp": self.timestamp, 'Message': self.messages})
            if self.users is not None:
                self.data['User'] = self.users
            self.data['Date'] = self.data['TimeStamp'].dt.strftime('%d-%b-%Y')
            self.data['Weekday'] = self.data['TimeStamp'].dt.strftime('%A')

    @staticmethod
    def remove_emoticons(text):
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
        return text

    @staticmethod
    def return_emoticons(text, sep = ";"):
        """
        Returns emoticons seperated by ";" from text
        :param text:
        :return:
        """
        emoji_pattern = re.compile("["
                                   "\U0001F600-\U0001F64F"  # emoticons
                                   "\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   "\U0001F680-\U0001F6FF"  # transport & map symbols
                                   "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
        emoticons = re.findall(emoji_pattern, text)
        emoticons_str = "".join(emoticons)
        emoticons_ct = len(list(emoticons_str))
        emoticons_str = sep.join(list(emoticons_str))
        return emoticons_str, emoticons_ct

    @staticmethod
    def remove_links(text):
        """
        Remove http/https links from message
        :param text:
        :return:
        """
        links_pattern = re.compile(r"http\S+", flags = re.UNICODE)
        links_ct = len(re.findall(links_pattern, text))
        text = links_pattern.sub(r'', text).strip()
        return text

    @staticmethod
    def return_links(text, sep = ";"):
        """
        Retunrs http/https links from message
        :param text:
        :return:
        """
        links_pattern = re.compile(r"http\S+", flags = re.UNICODE)
        links = re.findall(links_pattern, text)
        links_str = sep.join(links)
        links_ct = len(links)
        return links_str, links_ct

    @staticmethod
    def remove_media(text):
        """
        <Media omitted> in text, then return blank
        :param text:
        :return:
        """
        if text.strip() == "<Media omitted>":
            return ""
        else:
            return text

    @staticmethod
    def remove_unicode(text):
        """
        :param text:
        :return:
        """
        return text.encode('ascii', 'ignore').decode('utf-8')

    @staticmethod
    def remove_deleted_message(text):
        """

        :param text:
        :return:
        """
        if "deleted this message" in text.strip():
            return ""
        elif "message deleted" in text.strip():
            return ""
        else:
            return text

    @staticmethod
    def remove_missed_calls(text):
        """
        Missed voice/video call in text, then return blank
        :param text:
        :return:
        """
        if text.strip() == "Missed video call" or text.strip() == "Missed voice call":
            return ""
        else:
            return text

    @staticmethod
    def remove_punctuation(text):
        """

        :param text:
        :return:
        """
        return "".join([c for c in text if c not in string.punctuation])

    def get_clean_messages(self):
        """
        Clean the messages
        - Remove Emojis
        - Remove URLs
        - Remove media
        :return:
        """
        self.logger.write_logger('In user.py (get_clean_messages): Cleaning of messages starts')
        self.data['Clean Message'] = self.data['Message'].apply(lambda x: self.remove_media(x))
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_unicode(x))
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_deleted_message(x))
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_missed_calls(x))
        self.logger.write_logger('In user.py (remove_emoticons): Removing punctuation starts')
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_punctuation(x))
        self.logger.write_logger('In user.py (remove_emoticons): Removing punctuation ends')
        self.logger.write_logger('In user.py (remove_emoticons): Removing emoticons starts')
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_emoticons(x))
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: x.replace("✋", ""))
        self.logger.write_logger('In user.py (remove_emoticons): Removing emoticons ends')
        self.logger.write_logger('In user.py (remove_links): Removing links starts')
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: self.remove_links(x))
        self.logger.write_logger('In user.py (remove_links): Removing links ends')
        self.data['Clean Message'] = self.data['Clean Message'].apply(lambda x: x.lower())
        self.logger.write_logger('In user.py (get_clean_messages): Cleaning of messages ends')
        return self

    def get_message_sentiment(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_message_sentiment): Fetching the Sentiment of messages starts')
        self.data['Polarity Score'] = self.data['Clean Message'].apply(lambda x: Sentiment.vader(x))
        self.logger.write_logger('In user.py (get_message_sentiment): Fetching the Sentiment of messages ends')
        return self

    def get_top_sentiments(self, k = 2):
        """

        :param k:
        :return:
        """
        self.logger.write_logger(f'In user.py (get_top_sentiments): Fetching Top {k} Sentiments starts')
        top_k_positive = self.data[self.data['Polarity Score'] > 0]
        top_k_positive.sort_values('Polarity Score', ascending = False, inplace = True)
        if top_k_positive.shape[0] >= k:
            self.top_k_positive_str = "<br/><br/>".join(top_k_positive['Clean Message'].tolist()[:k])
        else:
            self.top_k_positive_str = ""

        top_k_negative = self.data[self.data['Polarity Score'] < 0]
        top_k_negative.sort_values('Polarity Score', ascending = True, inplace = True)
        if top_k_negative.shape[0] >= k:
            self.top_k_negative_str = "<br/><br/>".join(top_k_negative['Clean Message'].tolist()[:k])
        else:
            self.top_k_negative_str = ""
        self.data['Polarity Score'] = self.data['Clean Message'].apply(lambda x: Sentiment.vader(x))
        self.logger.write_logger(f'In user.py (get_top_sentiments): Fetching Top {k} Sentiments ends')
        return self

    @staticmethod
    def count_media(text):
        """

        :param text:
        :return:
        """
        if "<Media omitted>" in text:
            return 1
        else:
            return 0

    def get_media_count(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_media_count): Counting media starts')
        self.data['Media Count'] = self.data['Message'].apply(lambda x: self.count_media(x))
        self.logger.write_logger('In user.py (get_media_count): Counting media ends')
        return self

    def get_emoji_count(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_emoji_count): Counting of emoji starts')
        self.data['Emoji'] = self.data['Message'].apply(lambda x: self.return_emoticons(x)[0])
        self.data['Emoji Count'] = self.data['Message'].apply(lambda x: self.return_emoticons(x)[1])
        self.logger.write_logger('In user.py (get_emoji_count): Counting of emoji ends')
        return self

    def get_link_count(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_link_count): Counting of links starts')
        self.data['Links'] = self.data['Message'].apply(lambda x: self.return_links(x)[0])
        self.data['Links Count'] = self.data['Message'].apply(lambda x: self.return_links(x)[1])
        self.logger.write_logger('In user.py (get_link_count): Counting of links ends')
        return self

    @staticmethod
    def create_n_grams(doc_list, n_grams = 2):
        """

        :param doc_list:
        :param n_grams:
        :return:
        """
        n_gram_list = []
        for line in doc_list:
            tokens = line.split()
            tokens = User.lower_case_words(tokens)
            tokens = User.club_telugu_words(words = tokens)
            tokens = User.remove_stop_words(words = tokens)
            n_gram_words = [' '.join(v) for v in list(ngrams(tokens, n_grams))]
            n_gram_list.extend(n_gram_words)
        return n_gram_list

    @staticmethod
    def tokenize_words(doc):
        """

        :return:
        """

        words = " ".join(doc).split()
        words = User.lower_case_words(words)
        words = User.club_telugu_words(words = words)
        words = User.remove_stop_words(words = words)
        bigrams = User.create_n_grams(doc_list = doc, n_grams = 2)
        trigrams = User.create_n_grams(doc_list = doc, n_grams = 3)
        words = [w for w in words if len(w) > 3]
        return words, bigrams, trigrams

    @staticmethod
    def remove_stop_words(words):
        """

        :return:
        """
        stopwords_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                          "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                          'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                          'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                          'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                          'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                          'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                          'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                          'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                          'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                          'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                          'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
                          'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                          "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
                          "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
                          'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
                          "wouldn't"]
        words = [word for word in words if word not in stopwords_list]
        words = [word for word in words if word not in ['haan', 'okay', 'hahaha', 'tc', 'sd']]
        return words

    @staticmethod
    def lower_case_words(words):
        """

        :param words:
        :return:
        """
        return [word.lower() for word in words]

    @staticmethod
    def club_telugu_words(words):
        """

        :param words:
        :return:
        """
        clean_words = User.club_words(words = words, word1 = 'haha', word2 = 'hahaha')

        clean_words = User.club_words(words = clean_words, word1 = 'gud', word2 = 'good')
        clean_words = User.club_words(words = clean_words, word1 = 'gd', word2 = 'good')

        clean_words = User.club_words(words = clean_words, word1 = 'chasthunnau', word2 = 'chesthunnav')
        clean_words = User.club_words(words = clean_words, word1 = 'chasthunnaru', word2 = 'chesthunnav')
        clean_words = User.club_words(words = clean_words, word1 = 'chasthunnav', word2 = 'chesthunnav')

        clean_words = User.club_words(words = clean_words, word1 = 'kartu', word2 = 'kartheek')
        clean_words = User.club_words(words = clean_words, word1 = 'karteek', word2 = 'kartheek')
        clean_words = User.club_words(words = clean_words, word1 = 'karthu', word2 = 'kartheek')

        clean_words = User.club_words(words = clean_words, word1 = 'em', word2 = 'emi')

        clean_words = User.club_words(words = clean_words, word1 = 'unav', word2 = 'unavu')

        clean_words = User.club_words(words = clean_words, word1 = 'nv', word2 = 'nuvvu')
        clean_words = User.club_words(words = clean_words, word1 = 'nuv', word2 = 'nuvvu')
        clean_words = User.club_words(words = clean_words, word1 = 'nuvu', word2 = 'nuvvu')
        clean_words = User.club_words(words = clean_words, word1 = 'nuvu', word2 = 'nuvvu')

        clean_words = User.club_words(words = clean_words, word1 = 'k', word2 = 'okay')
        clean_words = User.club_words(words = clean_words, word1 = 'ok', word2 = 'okay')

        clean_words = User.club_words(words = clean_words, word1 = 'd', word2 = 'the')

        clean_words = User.club_words(words = clean_words, word1 = 'ade', word2 = 'adhe')
        clean_words = User.club_words(words = clean_words, word1 = 'adhey', word2 = 'adhe')

        clean_words = User.club_words(words = clean_words, word1 = 'na', word2 = 'naa')
        clean_words = User.club_words(words = clean_words, word1 = 'nee', word2 = 'ne')

        clean_words = User.club_words(words = clean_words, word1 = 'grp', word2 = 'group')

        clean_words = User.club_words(words = clean_words, word1 = 'nyt', word2 = 'night')
        clean_words = User.club_words(words = clean_words, word1 = 'nt', word2 = 'night')
        clean_words = User.club_words(words = clean_words, word1 = 'n8', word2 = 'night')

        clean_words = User.club_words(words = clean_words, word1 = 'haa', word2 = 'haan')
        clean_words = User.club_words(words = clean_words, word1 = 'ha', word2 = 'haan')

        clean_words = User.club_words(words = clean_words, word1 = 'gaa', word2 = 'ga')

        clean_words = User.club_words(words = clean_words, word1 = 'koda', word2 = 'kuda')
        clean_words = User.club_words(words = clean_words, word1 = 'kodaa', word2 = 'kuda')
        clean_words = User.club_words(words = clean_words, word1 = 'kudaa', word2 = 'kuda')
        clean_words = User.club_words(words = clean_words, word1 = 'kooda', word2 = 'kuda')

        clean_words = User.club_words(words = clean_words, word1 = 'aite', word2 = 'aithey')
        clean_words = User.club_words(words = clean_words, word1 = 'aithe', word2 = 'aithey')
        clean_words = User.club_words(words = clean_words, word1 = 'aitey', word2 = 'aithey')

        clean_words = User.club_words(words = clean_words, word1 = 'call', word2 = 'call')
        clean_words = User.club_words(words = clean_words, word1 = 'nen', word2 = 'nenu')

        clean_words = User.club_words(words = clean_words, word1 = 'kada', word2 = 'kadha')
        clean_words = User.club_words(words = clean_words, word1 = 'kadaa', word2 = 'kadha')
        clean_words = User.club_words(words = clean_words, word1 = 'kadhaa', word2 = 'kadha')

        clean_words = User.club_words(words = clean_words, word1 = 'e', word2 = 'ee')
        clean_words = User.club_words(words = clean_words, word1 = 'eee', word2 = 'ee')

        clean_words = User.club_words(words = clean_words, word1 = 'loo', word2 = 'lo')

        clean_words = User.club_words(words = clean_words, word1 = 'u', word2 = 'you')

        clean_words = User.club_words(words = clean_words, word1 = 'raa', word2 = 'ra')

        clean_words = User.club_words(words = clean_words, word1 = 'hmmm', word2 = 'hmm')
        clean_words = User.club_words(words = clean_words, word1 = 'hmmmm', word2 = 'hmm')

        clean_words = User.club_words(words = clean_words, word1 = 'lyt', word2 = 'light')
        return clean_words

    @staticmethod
    def club_words(words, word1, word2):
        """

        :param words:
        :param word1:
        :param word2:
        :return:
        """
        return [word2 if word == word1 else word for word in words]

    @staticmethod
    def prepare_month_df(min_year, max_year):
        """

        :param min_year:
        :param max_year:
        :return:
        """
        months = []
        for year in range(min_year, (max_year + 1)):
            for month in range(1, 13):
                if month < 10:
                    month = f"0{month}"
                else:
                    month = f"{month}"
                months.append(f"({year}) {month}")
        return pd.DataFrame({'Month': months})

    @staticmethod
    def lemmatize_and_stem(words, lemmatize_flag = True):
        """

        :param words:
        :param lemmatize_flag:
        :return:
        """
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        if lemmatize_flag:
            words = [lemmatizer.lemmatize(w) for w in words]
        else:
            words = [stemmer.stem(w) for w in words]
        return words

    def prepare_word_statistics(self):
        """
        Clean the clean messages
        - Create clean word list, clean double word list from the word list
        - Remove stop words
        :return:
        """
        # doc = " ".join(self.data[self.data['Clean Message'] != ""]['Clean Message'].tolist())
        doc = self.data[self.data['Clean Message'] != ""]['Clean Message'].tolist()
        # Tokenize ==========================================================================
        self.logger.write_logger('In user.py (prepare_word_statistics): Tokenization starts')
        self.words, self.bigrams, self.trigrams = self.tokenize_words(doc)
        self.logger.write_logger(
            f'\tFound {len(self.words)} words, {len(self.bigrams)} bigram words, {len(self.trigrams)} trigram words')
        self.logger.write_logger('In user.py (prepare_word_statistics): Tokenization ends')

        # Remove stop words =================================================================
        self.logger.write_logger('In user.py (prepare_word_statistics): Stop word removal starts')
        self.logger.write_logger('In user.py (prepare_word_statistics): Stop word removal ends')

        # Lemmatize and Stem the words ======================================================
        self.logger.write_logger('In user.py (prepare_word_statistics): Stemming and Lemmatization starts')
        self.clean_words = self.lemmatize_and_stem(self.words)
        self.clean_bigrams = self.lemmatize_and_stem(self.bigrams)
        self.clean_trigrams = self.lemmatize_and_stem(self.trigrams)
        self.logger.write_logger('In user.py (get_word_statistics): Stemming and Lemmatization ends')

        pd_word_df = pd.DataFrame({"Word": self.clean_words})
        pd_bigrams_df = pd.DataFrame({"Word": self.clean_bigrams})
        pd_trigrams_df = pd.DataFrame({"Word": self.clean_trigrams})
        return pd_word_df, pd_bigrams_df, pd_trigrams_df

    def get_word_statistics(self):
        """
        :return:
        """
        # Statistics ========================================================================
        self.logger.write_logger('In user.py (get_word_statistics): Formulating Word Statistics starts')
        self.pd_word_df, self.pd_bigrams_df, self.pd_trigrams_df = self.prepare_word_statistics()

        most_used_word = self.pd_word_df['Word'].value_counts().reset_index()['index'].tolist()[0]
        most_used_double_word = self.pd_bigrams_df['Word'].value_counts().reset_index()['index'].tolist()[0]
        most_used_triple_word = self.pd_trigrams_df['Word'].value_counts().reset_index()['index'].tolist()[0]
        self.most_used_word = {
            "Word" : most_used_word,
            "Count": self.pd_word_df[self.pd_word_df['Word'] == most_used_word].shape[0]
        }
        self.most_used_double_word = {
            "Word" : most_used_double_word,
            "Count": self.pd_bigrams_df[self.pd_bigrams_df['Word'] == most_used_double_word].shape[0]
        }
        self.most_used_triple_word = {
            "Word" : most_used_triple_word,
            "Count": self.pd_trigrams_df[self.pd_trigrams_df['Word'] == most_used_triple_word].shape[0]
        }
        self.logger.write_logger('In user.py (get_word_statistics): Formulating Word Statistics ends')

    def create_emoji_statistics(self):
        """

        :return:
        """
        _tmp_emoji_str = ";".join(self.data[self.data['Emoji'] != '']['Emoji'].tolist())
        self.emoji_list = _tmp_emoji_str.split(";")
        self.pd_emoji_df = pd.DataFrame({"Emoji": self.emoji_list})

    def get_emoji_statistics(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_emoji_statistics): Formulating Emoji Statistics starts')
        self.create_emoji_statistics()
        most_used_emoji = self.pd_emoji_df['Emoji'].value_counts().reset_index()['index'].tolist()[0]
        self.most_used_emoji = {
            "Emoji": most_used_emoji,
            "Count": self.pd_emoji_df[self.pd_emoji_df['Emoji'] == most_used_emoji].shape[0]
        }
        self.logger.write_logger('In user.py (get_emoji_statistics): Formulating Emoji Statistics ends')
        return self

    def get_total_stats(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_total_stats): Formulating Totals Statistics starts')
        self.get_word_statistics()
        self.n_messages = self.data.shape[0]
        self.n_words = len(self.words)
        self.n_unique_words = len(set(self.words))
        self.n_links = sum(self.data['Links Count'])
        self.n_emoji = sum(self.data['Emoji Count'])
        self.n_screen_touches = len(" ".join(self.words))  # counts number of characters

        first_msg_date = min(self.data.TimeStamp).strftime('%d-%b-%Y')
        recent_msg_date = max(self.data.TimeStamp).strftime('%d-%b-%Y')
        self.first_msg_date = {
            "Date"      : first_msg_date,
            "N_Messages": self.data[self.data['Date'] == first_msg_date].shape[0]
        }
        self.recent_msg_date = {
            "Date"      : recent_msg_date,
            "N_Messages": self.data[self.data['Date'] == recent_msg_date].shape[0]
        }

        _tmp_grouped_data = self.data.groupby(['Date'])['Message'].count().reset_index()
        most_active_date = _tmp_grouped_data.sort_values('Message', ascending = False)['Date'].tolist()[0]
        least_active_date = _tmp_grouped_data.sort_values('Message', ascending = True)['Date'].tolist()[0]
        self.most_active_date = {
            "Date"      : most_active_date,
            "N_Messages": self.data[self.data['Date'] == most_active_date].shape[0]
        }
        self.least_active_date = {
            "Date"      : least_active_date,
            "N_Messages": self.data[self.data['Date'] == least_active_date].shape[0]
        }

        self.n_days = (max(self.data.TimeStamp) - min(
            self.data.TimeStamp)).days  # Get start date and recent date, calculate difference
        self.n_days_chatted = len(set(self.data.Date))
        self.logger.write_logger('In user.py (get_total_stats): Formulating Totals Statistics ends')
        return self

    def get_avg_stats(self):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_avg_stats): Formulating Average Statistics starts')
        self.avg_messages_per_day = np.round(np.mean(
            self.data.groupby(['Date'])['Message'].count().reset_index()['Message'].tolist()
        ))
        self.avg_emojis_per_day = np.round(np.mean(
            self.data.groupby(['Date'])['Emoji Count'].sum().reset_index()['Emoji Count'].tolist()
        ))
        self.avg_links_per_day = np.ceil(np.mean(
            self.data.groupby(['Date'])['Links Count'].sum().reset_index()['Links Count'].tolist()
        ))
        self.data['Word Count'] = self.data['Clean Message'].apply(lambda x: len(x.split()))
        self.data['Letter Count'] = self.data['Clean Message'].apply(lambda x: len(x))
        self.avg_words_per_message = np.round(np.mean(self.data['Word Count']))
        self.avg_letters_per_message = np.round(np.mean(self.data['Letter Count']))
        self.logger.write_logger('In user.py (get_avg_stats): Formulating Average Statistics ends')
        return self

    def get_top_stats(self, data):
        """

        :return:
        """
        self.logger.write_logger('In user.py (get_top_stats): Formulating Top Statistics starts')
        _tmp_grouped_data = self.data.groupby(['Date'])['Message'].count().reset_index()
        self.logger.write_logger('\tIn user.py (get_top_stats): Formulating Active Day Statistics starts')
        most_active_date = _tmp_grouped_data.sort_values('Message', ascending = False)['Date'].tolist()[0]
        self.top_active_day = {
            'Date'          : most_active_date,
            'N_Messages'    : self.data[self.data['Date'] == most_active_date].shape[0],
            'Duration (Min)': ((max(self.data[self.data['Date'] == most_active_date]['TimeStamp']) - min(
                self.data[self.data['Date'] == most_active_date]['TimeStamp'])).seconds // 60) % 60,
            'N Words'       : sum(self.data[self.data['Date'] == most_active_date]['Word Count']),
            'N Emojis'      : sum(self.data[self.data['Date'] == most_active_date]['Emoji Count'])
        }  # more messages
        self.logger.write_logger('\tIn user.py (get_top_stats): Formulating Active Day Statistics ends')

        self.logger.write_logger('\tIn user.py (get_top_stats): Formulating Longest Conversation Day Statistics starts')
        response_obj = Response(data = data, logger = self.logger)
        longest_conversation_date = response_obj.get_the_longest_conversation_date()

        self.longest_conversation_day = {
            'Date'          : longest_conversation_date,
            'N_Messages'    : self.data[self.data['Date'] == longest_conversation_date].shape[0],
            'Duration (Min)': ((max(self.data[self.data['Date'] == longest_conversation_date]['TimeStamp']) - min(
                self.data[self.data['Date'] == longest_conversation_date]['TimeStamp'])).seconds // 60) % 60,
            'N Words'       : sum(self.data[self.data['Date'] == longest_conversation_date]['Word Count']),
            'N Emojis'      : sum(self.data[self.data['Date'] == longest_conversation_date]['Emoji Count'])
        }  # more time
        self.logger.write_logger('\tIn user.py (get_top_stats): Formulating Longest Conversation Day Statistics ends')
        self.logger.write_logger('In user.py (get_top_stats): Formulating Top Statistics ends')
        return self

    def get_response_time(self, data = None):
        """

        :param data:
        :return:
        """
        self.logger.write_logger(f'In user.py (get_response_time): Fetching response time starts')
        response_obj = Response(data = data, logger = self.logger)
        response_obj.group_the_data(). \
            create_response_time()
        if self.user_name != 'Overall':
            response_time = response_obj.grouped_data[
                (response_obj.grouped_data['User'] == self.user_name) & (
                        response_obj.grouped_data['Response (Min)'] > 0)][
                'Response (Min)']
        else:
            response_time = response_obj.grouped_data[(response_obj.grouped_data['Response (Min)'] > 0)][
                'Response (Min)']
        self.avg_response_time = np.round(stats.hmean(response_time), 3)
        self.logger.write_logger(f'In user.py (get_response_time): Fetching response time ends')
        return self

    def get_top_k_words(self, n_grams = 1, k = 20, normalize = True):
        """
        :param bigram_flag:
        :param k:
        :return:
        """
        self.logger.write_logger(f'In user.py (get_top_k_words): Fetching top {k} Words starts')
        if self.pd_word_df is None or self.pd_bigrams_df is None:
            self.pd_word_df, self.pd_bigrams_df, self.pd_trigrams_df = self.prepare_word_statistics()
        if n_grams == 2:
            _tmp_df = self.pd_bigrams_df.copy()
        elif n_grams == 1:
            _tmp_df = self.pd_word_df.copy()
        else:
            _tmp_df = self.pd_trigrams_df.copy()
        self.logger.write_logger(f'In user.py (get_top_k_words): Fetching top {k} Words ends')
        return _tmp_df['Word'].value_counts(normalize = normalize).head(k).reset_index().rename(
            columns = {'index': 'Word', 'Word': 'Count'})

    def get_top_k_emojis(self, k = 20, normalize = True):
        """

        :param k:
        :return:
        """
        self.logger.write_logger(f'In user.py (get_top_k_emojis): Fetching top {k} Emojis starts')
        if self.pd_emoji_df is None:
            self.create_emoji_statistics()
        self.logger.write_logger(f'In user.py (get_top_k_emojis): Fetching top {k} Emojis ends')
        return self.pd_emoji_df['Emoji'].value_counts(normalize = normalize).head(k).reset_index().rename(
            columns = {'index': 'Emoji', 'Emoji': 'Count'})

    def get_words_for_wordcloud(self, n_grams = 1):
        """

        :return:
        """
        self.logger.write_logger(f'In user.py (get_words_for_wordcloud): Fetching Words for WordCloud starts')
        if self.pd_word_df is None or self.pd_bigrams_df is None:
            self.pd_word_df, self.pd_bigrams_df, self.pd_trigrams_df = self.prepare_word_statistics()
        if n_grams == 1:
            words = self.pd_word_df['Word'].tolist()
        elif n_grams == 2:
            words = self.pd_bigrams_df['Word'].tolist()
            words = ["".join(w.title().split()) for w in words]
        else:
            words = self.pd_trigrams_df['Word'].tolist()
            words = ["".join(w.title().split()) for w in words]
        self.logger.write_logger(f'In user.py (get_words_for_wordcloud): Fetching  Words for WordCloud ends')
        return words

    def get_date_wise_n_msgs(self):
        """

        :return:
        """
        self.logger.write_logger(f'In user.py (get_date_wise_n_msgs): Fetching Datewise # of Msgs starts')
        result = self.data.groupby(['Date'])['Message'].count().reset_index()
        result['Date'] = pd.to_datetime(result['Date'], format = '%d-%b-%Y')
        result.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        result = result.sort_values(['Date'])
        result['Date'] = result['Date'].dt.strftime('%d-%b-%Y')
        self.logger.write_logger(f'In user.py (get_date_wise_n_msgs): Fetching Datewise # of Msgs ends')
        return result

    def get_domain_count(self):
        """

        :return:
        """
        self.logger.write_logger(f'In user.py (get_domain_count): Fetching Domains from links starts')
        pd_links_df = self.data[self.data['Links Count'] > 0][['User', 'Links']]
        pd_links_df['Links List'] = pd_links_df['Links'].apply(lambda x: x.split(";"))
        pd_links_df = pd_links_df.explode("Links List")
        pd_links_df['Links List'] = pd_links_df['Links List'].apply(lambda x: x.replace("https-", ""))
        pd_links_df['Links List'] = pd_links_df['Links List'].apply(lambda x: x.replace("http-", ""))
        pd_links_df['Links List'] = pd_links_df['Links List'].apply(lambda x: x.replace("https:", ""))
        pd_links_df['Links List'] = pd_links_df['Links List'].apply(lambda x: x.replace("http:", ""))
        pd_links_df['Domain'] = pd_links_df['Links List'].apply(lambda x: tldextract.extract(x).domain)
        pd_links_df = pd_links_df.groupby(['User', 'Domain'])['Links List'].count().reset_index()
        pd_links_df.rename(columns = {'Links List': 'Count'}, inplace = True)
        self.logger.write_logger(f'In user.py (get_domain_count): Fetching Domains from links ends')
        return pd_links_df

    def get_userwise_emoji_count(self):
        """

        :return:
        """
        self.logger.write_logger(f'In user.py (get_userwise_emoji_count): Fetching Userwise Emoji Count starts')
        pd_emojis_df = self.data[['User', 'Emoji Count', 'TimeStamp', 'Date']]
        pd_emojis_df = pd_emojis_df.groupby(['Date', 'User'])['Emoji Count'].sum().reset_index()
        self.logger.write_logger(f'In user.py (get_userwise_emoji_count): Fetching Userwise Emoji Count ends')
        return pd_emojis_df

    def get_date_wise_avg_words(self):
        """

        :return:
        """
        pass

    def get_userwise_monthly_word_counts(self):
        """

        :return:
        """
        _tmp = self.data.copy()
        _tmp['Month'] = _tmp['TimeStamp'].dt.strftime('(%Y) %m')
        pd_monthly_word_counts = _tmp.groupby(['Month', 'User'])['Word Count'].mean().reset_index()
        pd_monthly_word_counts.sort_values(['User', 'Month'], inplace = True)
        return pd_monthly_word_counts

    def get_userwise_monthly_emoji_counts(self):
        """

        :return:
        """
        _tmp = self.data.copy()
        _tmp['Month'] = _tmp['TimeStamp'].dt.strftime('(%Y) %m')
        pd_monthly_emoji_counts = _tmp.groupby(['Month', 'User'])['Emoji Count'].mean().reset_index()
        pd_monthly_emoji_counts.sort_values(['User', 'Month'], inplace = True)
        return pd_monthly_emoji_counts

    @staticmethod
    def harmonic_mean(x):
        """

        :param x:
        :return:
        """
        return stats.hmean([v for v in x if v > 0])

    def get_userwise_monthly_response_time(self, data):
        """

        :return:
        """
        response_obj = Response(data = data, logger = self.logger)
        response_obj.group_the_data(). \
            create_response_time()
        response_obj.grouped_data['Month'] = response_obj.grouped_data['Timestamp'].dt.strftime('(%Y) %m')
        userwise_monthly_response_time = response_obj.grouped_data.groupby(['Month', 'User'])[
            'Response (Min)'].agg(User.harmonic_mean).reset_index()
        userwise_monthly_response_time.loc[userwise_monthly_response_time['Response (Min)'] > 60, 'Response (Min)'] = -1
        userwise_monthly_response_time.sort_values(['User', 'Month'], inplace = True)
        return userwise_monthly_response_time

    def get_first_text_monthly_count(self):
        """

        :param data:
        :return:
        """
        _tmp = self.data.copy()
        _tmp = _tmp.sort_values(['TimeStamp'])
        _tmp['Date'] = _tmp['TimeStamp'].dt.strftime('%d-%b-%Y')
        _tmp['Hour'] = _tmp['TimeStamp'].dt.hour
        # Used to filter texting after waking up rather than during the mid night conversation
        _tmp = _tmp[_tmp.Hour > 6]
        grp_tmp = _tmp.groupby(['Date'])['User'].first().reset_index()
        grp_tmp['TimeStamp'] = pd.to_datetime(grp_tmp['Date'], format = '%d-%b-%Y')
        grp_tmp = grp_tmp.sort_values(['TimeStamp'])
        grp_tmp['Month'] = grp_tmp['TimeStamp'].dt.strftime('(%Y) %m')
        pd_monthly_first_text_counts = grp_tmp.groupby(['Month', 'User'])['Date'].count().reset_index()
        pd_monthly_first_text_counts.sort_values(['User', 'Month'], inplace = True)
        return pd_monthly_first_text_counts

    def get_monthly_avg_polarity(self):
        """

        :return:
        """
        _tmp = self.data.copy()
        _tmp['Month'] = _tmp['TimeStamp'].dt.strftime('(%Y) %m')
        pd_monthly_avg_polarity = _tmp.groupby(['Month', 'User'])['Polarity Score'].mean().reset_index()
        pd_monthly_avg_polarity.sort_values(['User', 'Month'], inplace = True)
        return pd_monthly_avg_polarity