import base64
import math
import datetime
from action_logging import Logger


class HTMLImages:

    def __init__(self, save_path = "plots/", logger = None):
        """

        :param save_path:
        """
        # Link: https://stackoverflow.com/questions/7389567/output-images-to-html-using-python
        # data_uri = base64.b64encode(open('Graph.png', 'rb').read()).decode('utf-8')
        self.save_path = save_path
        self.logger = logger

        self.word_cloud_1words_u1 = None
        self.word_cloud_1words_u2 = None
        self.word_cloud_2words_u1 = None
        self.word_cloud_2words_u2 = None
        self.word_cloud_3words_u1 = None
        self.word_cloud_3words_u2 = None

        self.date_n_msgs = None
        self.date_n_emojis = None
        self.weekly_pattern = None
        self.hourly_pattern = None
        self.monthly_msg_pattern = None
        self.monthly_word_pattern = None
        self.monthly_emoji_pattern = None
        self.monthly_response_pattern = None
        self.domain_counts = None

    @staticmethod
    def encode_decode_img(image_path):
        """

        :param image_path:
        :return:
        """
        return f"data:image/png;base64,{base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')}"

    def populate_word_cloud(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLImages/populate_word_cloud): Populating Word Cloud")
        self.word_cloud_1words_u1 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_1words_u1.png")
        self.word_cloud_1words_u2 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_1words_u2.png")
        self.word_cloud_2words_u1 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_2words_u1.png")
        self.word_cloud_2words_u2 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_2words_u2.png")
        self.word_cloud_3words_u1 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_3words_u1.png")
        self.word_cloud_3words_u2 = HTMLImages.encode_decode_img(f"{self.save_path}/word_cloud_3words_u2.png")
        return self

    def populate_rest_images(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLImages/populate_rest_images): Populating Rest of the images")
        self.date_n_msgs = HTMLImages.encode_decode_img(f"{self.save_path}/date_n_msgs.png")
        self.date_n_emojis = HTMLImages.encode_decode_img(f"{self.save_path}/date_n_emojis.png")
        self.weekly_pattern = HTMLImages.encode_decode_img(f"{self.save_path}/weekday_n_msgs.png")
        self.hourly_pattern = HTMLImages.encode_decode_img(f"{self.save_path}/hour_n_msgs.png")
        self.monthly_msg_pattern = HTMLImages.encode_decode_img(f"{self.save_path}/monthly_msg_progression.png")
        self.monthly_word_pattern = HTMLImages.encode_decode_img(f"{self.save_path}/monthly_word_progression.png")
        self.monthly_emoji_pattern = HTMLImages.encode_decode_img(f"{self.save_path}/monthly_emoji_progression.png")
        self.monthly_response_pattern = HTMLImages.encode_decode_img(
            f"{self.save_path}/monthly_response_time_progression.png")
        self.monthly_first_text_ct = HTMLImages.encode_decode_img(f"{self.save_path}/monthly_first_text_ct.png")
        self.monthly_avg_polarity = HTMLImages.encode_decode_img(f"{self.save_path}/monthly_avg_polarity.png")
        self.domain_counts = HTMLImages.encode_decode_img(f"{self.save_path}/domain_counts.png")
        return self


class HTMLStats:

    def __init__(self, user1, user2, overall, logger = None):
        self.user1 = user1
        self.user2 = user2
        self.overall = overall
        self.logger = logger
        self.emoji1_u1 = ""
        self.emoji1_u2 = ""
        self.emoji2_u1 = ""
        self.emoji2_u2 = ""
        self.emoji3_u1 = ""
        self.emoji3_u2 = ""
        self.emoji4_u1 = ""
        self.emoji4_u2 = ""
        self.emoji5_u1 = ""
        self.emoji5_u2 = ""
        self.top_k_positive_u1 = ""
        self.top_k_positive_u2 = ""
        self.top_k_negative_u1 = ""
        self.top_k_negative_u2 = ""

    def populate_names(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_names): Populating names")
        self.user1_name = self.user1.user_name
        self.user2_name = self.user2.user_name
        return self

    def get_n_years(self):
        """

        :return:
        """
        return int(math.ceil(self.overall.n_days / 365))

    def populate_title(self):
        """
        Title = User1 <==> User2\nA N Year Journey
        :return:
        """
        self.title = "{user1} & {user2}"
        self.sup_title = "A {n_year} Year Journey"
        self.title = self.title.replace("{user1}", f"{self.user1_name}")
        self.title = self.title.replace("{user2}", f"{self.user2_name}")
        self.sup_title = self.sup_title.replace("{n_year}", f"{self.get_n_years()}")
        return self

    def populate_totals(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_totals): Populating totals")
        # Messages Sent
        self.n_msgs_u1 = self.user1.n_messages
        self.n_msgs_u2 = self.user2.n_messages
        self.n_msgs_overall = self.overall.n_messages
        # Words Used
        self.n_words_u1 = self.user1.n_words
        self.n_words_u2 = self.user2.n_words
        self.n_words_overall = self.overall.n_words
        # Unique words used
        self.n_unique_words_u1 = self.user1.n_unique_words
        self.n_unique_words_u2 = self.user2.n_unique_words
        self.n_unique_words_overall = self.overall.n_unique_words
        # Links Shared
        self.n_links_u1 = self.user1.n_links
        self.n_links_u2 = self.user2.n_links
        self.n_links_overall = self.overall.n_links
        # Emojis Sent
        self.n_emojis_u1 = self.user1.n_emoji
        self.n_emojis_u2 = self.user2.n_emoji
        self.n_emojis_overall = self.overall.n_emoji
        # Screen Touches
        self.n_touches_u1 = self.user1.n_screen_touches
        self.n_touches_u2 = self.user2.n_screen_touches
        self.n_touches_overall = self.overall.n_screen_touches
        # Days Texted (and %)
        self.n_days_texted_u1 = f"{self.user1.n_days_chatted} ({round((self.user1.n_days_chatted/self.user1.n_days)*100)} %)"
        self.n_days_texted_u2 = f"{self.user2.n_days_chatted} ({round((self.user2.n_days_chatted/self.user2.n_days)*100)} %)"
        self.n_days_texted_overall = f"{self.overall.n_days_chatted} ({round((self.overall.n_days_chatted/self.overall.n_days)*100)} %)"
        # Most Used Word
        self.word_u1 = self.user1.most_used_word['Word']
        self.word_u2 = self.user2.most_used_word['Word']
        self.word_overall = self.overall.most_used_word['Word']
        # Most Used Double Word
        self.double_word_u1 = self.user1.most_used_double_word['Word']
        self.double_word_u2 = self.user2.most_used_double_word['Word']
        self.double_word_overall = self.overall.most_used_double_word['Word']
        # Most Used Triple Word
        self.triple_word_u1 = self.user1.most_used_triple_word['Word']
        self.triple_word_u2 = self.user2.most_used_triple_word['Word']
        self.triple_word_overall = self.overall.most_used_triple_word['Word']
        # Most Used Emoji
        self.emoji_u1 = self.user1.most_used_emoji['Emoji']
        self.emoji_u2 = self.user2.most_used_emoji['Emoji']
        self.emoji_overall = self.overall.most_used_emoji['Emoji']
        # First Message Date
        self.first_msg_date_u1 = self.user1.first_msg_date['Date']
        self.first_msg_date_u2 = self.user2.first_msg_date['Date']
        self.first_msg_date_overall = self.overall.first_msg_date['Date']
        # Recent Message Date
        self.recent_msg_date_u1 = self.user1.recent_msg_date['Date']
        self.recent_msg_date_u2 = self.user2.recent_msg_date['Date']
        self.recent_msg_date_overall = self.overall.recent_msg_date['Date']
        # Most Active Date
        self.most_active_date_u1 = self.user1.most_active_date['Date']
        self.most_active_date_u2 = self.user2.most_active_date['Date']
        self.most_active_date_overall = self.overall.most_active_date['Date']
        # Least Active Date
        self.least_active_date_u1 = self.user1.least_active_date['Date']
        self.least_active_date_u2 = self.user2.least_active_date['Date']
        self.least_active_date_overall = self.overall.least_active_date['Date']
        return self

    def populate_averages(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_averages): Populating Averages")
        # Avg. Message/day
        self.avg_msgs_u1 = self.user1.avg_messages_per_day
        self.avg_msgs_u2 = self.user2.avg_messages_per_day
        self.avg_msgs_overall = self.overall.avg_messages_per_day
        # Avg. Emojis/day
        self.avg_emojis_u1 = self.user1.avg_emojis_per_day
        self.avg_emojis_u2 = self.user2.avg_emojis_per_day
        self.avg_emojis_overall = self.overall.avg_emojis_per_day
        # Avg. Links/day
        self.avg_links_u1 = self.user1.avg_links_per_day
        self.avg_links_u2 = self.user2.avg_links_per_day
        self.avg_links_overall = self.overall.avg_links_per_day
        # Avg. Words/Message
        self.avg_words_u1 = self.user1.avg_words_per_message
        self.avg_words_u2 = self.user2.avg_words_per_message
        self.avg_words_overall = self.overall.avg_words_per_message
        # Avg. Letters/Message
        self.avg_letters_u1 = self.user1.avg_letters_per_message
        self.avg_letters_u2 = self.user2.avg_letters_per_message
        self.avg_letters_overall = self.overall.avg_letters_per_message
        return self

    def populate_sentiments(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_sentiments): Populating Sentiments starts")
        self.top_k_positive_u1 = self.user1.top_k_positive_str
        self.top_k_positive_u2 = self.user2.top_k_positive_str

        self.top_k_negative_u1 = self.user1.top_k_negative_str
        self.top_k_negative_u2 = self.user2.top_k_negative_str

        self.logger.write_logger("In generate_html.py (HTMLStats/populate_sentiments): Populating Sentiments ends")
        return self


    def populate_tops(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_tops): Populating Tops")
        # Active Day - Date
        self.active_date_u1 = self.user1.top_active_day['Date']
        self.active_date_u2 = self.user2.top_active_day['Date']
        self.active_date_overall = self.overall.top_active_day['Date']
        # Active Day - Messages
        self.active_date_msgs_u1 = self.user1.top_active_day['N_Messages']
        self.active_date_msgs_u2 = self.user2.top_active_day['N_Messages']
        self.active_date_msgs_overall = self.overall.top_active_day['N_Messages']
        # Active Day Words
        self.active_date_words_u1 = self.user1.top_active_day['N Words']
        self.active_date_words_u2 = self.user2.top_active_day['N Words']
        self.active_date_words_overall = self.overall.top_active_day['N Words']
        # Active Day Duration
        self.active_date_duration_u1 = self.user1.top_active_day['Duration (Min)']
        self.active_date_duration_u2 = self.user2.top_active_day['Duration (Min)']
        self.active_date_duration_overall = self.overall.top_active_day['Duration (Min)']
        # Active Day Emojis
        self.active_date_emojis_u1 = self.user1.top_active_day['N Emojis']
        self.active_date_emojis_u2 = self.user2.top_active_day['N Emojis']
        self.active_date_emojis_overall = self.overall.top_active_day['N Emojis']
        # Longest Conversation Date
        self.lc_date_u1 = self.user1.longest_conversation_day['Date']
        self.lc_date_u2 = self.user2.longest_conversation_day['Date']
        self.lc_date_overall = self.overall.longest_conversation_day['Date']
        # Longest Conversation Messages
        self.lc_date_msgs_u1 = self.user1.longest_conversation_day['N_Messages']
        self.lc_date_msgs_u2 = self.user2.longest_conversation_day['N_Messages']
        self.lc_date_msgs_overall = self.overall.longest_conversation_day['N_Messages']
        # Longest Conversation Words
        self.lc_date_words_u1 = self.user1.longest_conversation_day['N Words']
        self.lc_date_words_u2 = self.user2.longest_conversation_day['N Words']
        self.lc_date_words_overall = self.overall.longest_conversation_day['N Words']
        # Longest Conversation Duration
        self.lc_date_duration_u1 = self.user1.longest_conversation_day['Duration (Min)']
        self.lc_date_duration_u2 = self.user2.longest_conversation_day['Duration (Min)']
        self.lc_date_duration_overall = self.overall.longest_conversation_day['Duration (Min)']
        # Longest Conversation Emojis
        self.lc_date_emojis_u1 = self.user1.longest_conversation_day['N Emojis']
        self.lc_date_emojis_u2 = self.user2.longest_conversation_day['N Emojis']
        self.lc_date_emojis_overall = self.overall.longest_conversation_day['N Emojis']
        return self

    def populate_response(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_response): Populating Response Times")
        self.avg_response_u1 = self.user1.avg_response_time
        self.avg_response_u2 = self.user2.avg_response_time
        self.avg_response_overall = self.overall.avg_response_time
        return self

    def populate_emoji_ranks(self):
        """

        :return:
        """
        self.logger.write_logger("In generate_html.py (HTMLStats/populate_emoji_ranks): Populating Emoji ranks")
        if self.user1.pd_emoji_rank.shape[0] == 5 and self.user2.pd_emoji_rank.shape[0] == 5:
            self.emoji1_u1 = self.user1.pd_emoji_rank['Emoji'].tolist()[0]
            self.emoji1_u2 = self.user2.pd_emoji_rank['Emoji'].tolist()[0]
            self.emoji2_u1 = self.user1.pd_emoji_rank['Emoji'].tolist()[1]
            self.emoji2_u2 = self.user2.pd_emoji_rank['Emoji'].tolist()[1]
            self.emoji3_u1 = self.user1.pd_emoji_rank['Emoji'].tolist()[2]
            self.emoji3_u2 = self.user2.pd_emoji_rank['Emoji'].tolist()[2]
            self.emoji4_u1 = self.user1.pd_emoji_rank['Emoji'].tolist()[3]
            self.emoji4_u2 = self.user2.pd_emoji_rank['Emoji'].tolist()[3]
            self.emoji5_u1 = self.user1.pd_emoji_rank['Emoji'].tolist()[4]
            self.emoji5_u2 = self.user2.pd_emoji_rank['Emoji'].tolist()[4]
        return self


class HTML:

    def __init__(self, user1, user2, overall, save_path = "plots/", html_path = "html_template/index.html",
                 logger = None):
        """

        :param user1:
        :param user2:
        :param overall:
        :param save_path:
        """
        self.user1 = user1
        self.user2 = user2
        self.overall = overall
        self.save_path = save_path
        self.html_path = html_path
        with open(self.html_path, 'r') as f:
            self.html_txt = f.read()
        if logger is None:
            self.logger = Logger(log_flag = True, log_file = "html", log_path = "../logs/")
        else:
            self.logger = logger

    def populate_members(self):
        """

        :return:
        """
        self.html_stats = HTMLStats(user1 = self.user1, user2 = self.user2, overall = self.overall,
                                    logger = self.logger)
        self.html_images = HTMLImages(save_path = self.save_path, logger = self.logger)

        self.html_images.populate_word_cloud(). \
            populate_rest_images()
        self.html_stats.populate_names(). \
            populate_title(). \
            populate_totals(). \
            populate_averages(). \
            populate_sentiments(). \
            populate_tops(). \
            populate_response(). \
            populate_emoji_ranks()
        return self

    def populate_html_txt(self):
        """

        :return:
        """
        # Title
        self.html_txt = self.html_txt.replace("{title}", f"{self.html_stats.title}")
        self.html_txt = self.html_txt.replace("{sup_title}", f"{self.html_stats.sup_title}")
        # User names
        self.html_txt = self.html_txt.replace("{user1}", f"{self.html_stats.user1_name}")
        self.html_txt = self.html_txt.replace("{user2}", f"{self.html_stats.user2_name}")
        # Messages Sent
        self.html_txt = self.html_txt.replace("{n_msgs_u1}", f"{self.html_stats.n_msgs_u1}")
        self.html_txt = self.html_txt.replace("{n_msgs_u2}", f"{self.html_stats.n_msgs_u2}")
        self.html_txt = self.html_txt.replace("{n_msgs_overall}", f"{self.html_stats.n_msgs_overall}")
        # Words Used
        self.html_txt = self.html_txt.replace("{n_words_u1}", f"{self.html_stats.n_words_u1}")
        self.html_txt = self.html_txt.replace("{n_words_u2}", f"{self.html_stats.n_words_u2}")
        self.html_txt = self.html_txt.replace("{n_words_overall}", f"{self.html_stats.n_words_overall}")
        # Unique words used
        self.html_txt = self.html_txt.replace("{n_unique_words_u1}", f"{self.html_stats.n_unique_words_u1}")
        self.html_txt = self.html_txt.replace("{n_unique_words_u2}", f"{self.html_stats.n_unique_words_u2}")
        self.html_txt = self.html_txt.replace("{n_unique_words_overall}", f"{self.html_stats.n_unique_words_overall}")
        # Links Shared
        self.html_txt = self.html_txt.replace("{n_links_u1}", f"{self.html_stats.n_links_u1}")
        self.html_txt = self.html_txt.replace("{n_links_u2}", f"{self.html_stats.n_links_u2}")
        self.html_txt = self.html_txt.replace("{n_links_overall}", f"{self.html_stats.n_links_overall}")
        # Emojis Sent
        self.html_txt = self.html_txt.replace("{n_emojis_u1}", f"{self.html_stats.n_emojis_u1}")
        self.html_txt = self.html_txt.replace("{n_emojis_u2}", f"{self.html_stats.n_emojis_u2}")
        self.html_txt = self.html_txt.replace("{n_emojis_overall}", f"{self.html_stats.n_emojis_overall}")
        # Screen Touches
        self.html_txt = self.html_txt.replace("{n_touches_u1}", f"{self.html_stats.n_touches_u1}")
        self.html_txt = self.html_txt.replace("{n_touches_u2}", f"{self.html_stats.n_touches_u2}")
        self.html_txt = self.html_txt.replace("{n_touches_overall}", f"{self.html_stats.n_touches_overall}")
        # Days Texted (and %)
        self.html_txt = self.html_txt.replace("{n_days_texted_u1}", f"{self.html_stats.n_days_texted_u1}")
        self.html_txt = self.html_txt.replace("{n_days_texted_u2}", f"{self.html_stats.n_days_texted_u2}")
        self.html_txt = self.html_txt.replace("{n_days_texted_overall}", f"{self.html_stats.n_days_texted_overall}")
        # Most Used Word
        self.html_txt = self.html_txt.replace("{word_u1}", f"{self.html_stats.word_u1}")
        self.html_txt = self.html_txt.replace("{word_u2}", f"{self.html_stats.word_u2}")
        self.html_txt = self.html_txt.replace("{word_overall}", f"{self.html_stats.word_overall}")
        # Most Used Double Word
        self.html_txt = self.html_txt.replace("{double_word_u1}", f"{self.html_stats.double_word_u1}")
        self.html_txt = self.html_txt.replace("{double_word_u2}", f"{self.html_stats.double_word_u2}")
        self.html_txt = self.html_txt.replace("{double_word_overall}", f"{self.html_stats.double_word_overall}")
        # Most Used Triple Word
        self.html_txt = self.html_txt.replace("{triple_word_u1}", f"{self.html_stats.triple_word_u1}")
        self.html_txt = self.html_txt.replace("{triple_word_u2}", f"{self.html_stats.triple_word_u2}")
        self.html_txt = self.html_txt.replace("{triple_word_overall}", f"{self.html_stats.triple_word_overall}")
        # Most Used Emoji
        self.html_txt = self.html_txt.replace("{emoji_u1}", f"{self.html_stats.emoji_u1}")
        self.html_txt = self.html_txt.replace("{emoji_u2}", f"{self.html_stats.emoji_u2}")
        self.html_txt = self.html_txt.replace("{emoji_overall}", f"{self.html_stats.emoji_overall}")
        # First Message Date
        self.html_txt = self.html_txt.replace("{first_msg_date_u1}", f"{self.html_stats.first_msg_date_u1}")
        self.html_txt = self.html_txt.replace("{first_msg_date_u2}", f"{self.html_stats.first_msg_date_u2}")
        self.html_txt = self.html_txt.replace("{first_msg_date_overall}", f"{self.html_stats.first_msg_date_overall}")
        # Recent Message Date
        self.html_txt = self.html_txt.replace("{recent_msg_date_u1}", f"{self.html_stats.recent_msg_date_u1}")
        self.html_txt = self.html_txt.replace("{recent_msg_date_u2}", f"{self.html_stats.recent_msg_date_u2}")
        self.html_txt = self.html_txt.replace("{recent_msg_date_overall}", f"{self.html_stats.recent_msg_date_overall}")
        # Most Active Date
        self.html_txt = self.html_txt.replace("{most_active_date_u1}", f"{self.html_stats.most_active_date_u1}")
        self.html_txt = self.html_txt.replace("{most_active_date_u2}", f"{self.html_stats.most_active_date_u2}")
        self.html_txt = self.html_txt.replace("{most_active_date_overall}",
                                              f"{self.html_stats.most_active_date_overall}")
        # Least Active Date
        self.html_txt = self.html_txt.replace("{least_active_date_u1}", f"{self.html_stats.least_active_date_u1}")
        self.html_txt = self.html_txt.replace("{least_active_date_u2}", f"{self.html_stats.least_active_date_u2}")
        self.html_txt = self.html_txt.replace("{least_active_date_overall}",
                                              f"{self.html_stats.least_active_date_overall}")
        # Avg. Message/day
        self.html_txt = self.html_txt.replace("{avg_msgs_u1}", f"{self.html_stats.avg_msgs_u1}")
        self.html_txt = self.html_txt.replace("{avg_msgs_u2}", f"{self.html_stats.avg_msgs_u2}")
        self.html_txt = self.html_txt.replace("{avg_msgs_overall}", f"{self.html_stats.avg_msgs_overall}")
        # Avg. Emojis/day
        self.html_txt = self.html_txt.replace("{avg_emojis_u1}", f"{self.html_stats.avg_emojis_u1}")
        self.html_txt = self.html_txt.replace("{avg_emojis_u2}", f"{self.html_stats.avg_emojis_u2}")
        self.html_txt = self.html_txt.replace("{avg_emojis_overall}", f"{self.html_stats.avg_emojis_overall}")
        # Avg. Links/day
        self.html_txt = self.html_txt.replace("{avg_links_u1}", f"{self.html_stats.avg_links_u1}")
        self.html_txt = self.html_txt.replace("{avg_links_u2}", f"{self.html_stats.avg_links_u2}")
        self.html_txt = self.html_txt.replace("{avg_links_overall}", f"{self.html_stats.avg_links_overall}")
        # Avg. Words/Message
        self.html_txt = self.html_txt.replace("{avg_words_u1}", f"{self.html_stats.avg_words_u1}")
        self.html_txt = self.html_txt.replace("{avg_words_u2}", f"{self.html_stats.avg_words_u2}")
        self.html_txt = self.html_txt.replace("{avg_words_overall}", f"{self.html_stats.avg_words_overall}")
        # Avg. Letters/Message
        self.html_txt = self.html_txt.replace("{avg_letters_u1}", f"{self.html_stats.avg_letters_u1}")
        self.html_txt = self.html_txt.replace("{avg_letters_u2}", f"{self.html_stats.avg_letters_u2}")
        self.html_txt = self.html_txt.replace("{avg_letters_overall}", f"{self.html_stats.avg_letters_overall}")
        # Active Day - Date
        self.html_txt = self.html_txt.replace("{active_date_u1}", f"{self.html_stats.active_date_u1}")
        self.html_txt = self.html_txt.replace("{active_date_u2}", f"{self.html_stats.active_date_u2}")
        self.html_txt = self.html_txt.replace("{active_date_overall}", f"{self.html_stats.active_date_overall}")
        # Active Day - Messages
        self.html_txt = self.html_txt.replace("{active_date_msgs_u1}", f"{self.html_stats.active_date_msgs_u1}")
        self.html_txt = self.html_txt.replace("{active_date_msgs_u2}", f"{self.html_stats.active_date_msgs_u2}")
        self.html_txt = self.html_txt.replace("{active_date_msgs_overall}",
                                              f"{self.html_stats.active_date_msgs_overall}")
        # Active Day Words
        self.html_txt = self.html_txt.replace("{active_date_words_u1}", f"{self.html_stats.active_date_words_u1}")
        self.html_txt = self.html_txt.replace("{active_date_words_u2}", f"{self.html_stats.active_date_words_u2}")
        self.html_txt = self.html_txt.replace("{active_date_words_overall}",
                                              f"{self.html_stats.active_date_words_overall}")
        # Active Day Duration
        self.html_txt = self.html_txt.replace("{active_date_duration_u1}", f"{self.html_stats.active_date_duration_u1}")
        self.html_txt = self.html_txt.replace("{active_date_duration_u2}", f"{self.html_stats.active_date_duration_u2}")
        self.html_txt = self.html_txt.replace("{active_date_duration_overall}",
                                              f"{self.html_stats.active_date_duration_overall}")
        # Active Day Emojis
        self.html_txt = self.html_txt.replace("{active_date_emojis_u1}", f"{self.html_stats.active_date_emojis_u1}")
        self.html_txt = self.html_txt.replace("{active_date_emojis_u2}", f"{self.html_stats.active_date_emojis_u2}")
        self.html_txt = self.html_txt.replace("{active_date_emojis_overall}",
                                              f"{self.html_stats.active_date_emojis_overall}")
        # Longest Conversation Date
        self.html_txt = self.html_txt.replace("{lc_date_u1}", f"{self.html_stats.lc_date_u1}")
        self.html_txt = self.html_txt.replace("{lc_date_u2}", f"{self.html_stats.lc_date_u2}")
        self.html_txt = self.html_txt.replace("{lc_date_overall}", f"{self.html_stats.lc_date_overall}")
        # Longest Conversation Messages
        self.html_txt = self.html_txt.replace("{lc_date_msgs_u1}", f"{self.html_stats.lc_date_msgs_u1}")
        self.html_txt = self.html_txt.replace("{lc_date_msgs_u2}", f"{self.html_stats.lc_date_msgs_u2}")
        self.html_txt = self.html_txt.replace("{lc_date_msgs_overall}", f"{self.html_stats.lc_date_msgs_overall}")
        # Longest Conversation Words
        self.html_txt = self.html_txt.replace("{lc_date_words_u1}", f"{self.html_stats.lc_date_words_u1}")
        self.html_txt = self.html_txt.replace("{lc_date_words_u2}", f"{self.html_stats.lc_date_words_u2}")
        self.html_txt = self.html_txt.replace("{lc_date_words_overall}", f"{self.html_stats.lc_date_words_overall}")
        # Longest Conversation Duration
        self.html_txt = self.html_txt.replace("{lc_date_duration_u1}", f"{self.html_stats.lc_date_duration_u1}")
        self.html_txt = self.html_txt.replace("{lc_date_duration_u2}", f"{self.html_stats.lc_date_duration_u2}")
        self.html_txt = self.html_txt.replace("{lc_date_duration_overall}",
                                              f"{self.html_stats.lc_date_duration_overall}")
        # Longest Conversation Emojis
        self.html_txt = self.html_txt.replace("{lc_date_emojis_u1}", f"{self.html_stats.lc_date_emojis_u1}")
        self.html_txt = self.html_txt.replace("{lc_date_emojis_u2}", f"{self.html_stats.lc_date_emojis_u2}")
        self.html_txt = self.html_txt.replace("{lc_date_emojis_overall}", f"{self.html_stats.lc_date_emojis_overall}")
        # Response time stats
        self.html_txt = self.html_txt.replace("{avg_response_u1}", f"{self.html_stats.avg_response_u1}")
        self.html_txt = self.html_txt.replace("{avg_response_u2}", f"{self.html_stats.avg_response_u2}")
        self.html_txt = self.html_txt.replace("{avg_response_overall}", f"{self.html_stats.avg_response_overall}")
        # Top Sentiments
        self.html_txt = self.html_txt.replace("{top_k_positive_u1}", f"{self.html_stats.top_k_positive_u1}")
        self.html_txt = self.html_txt.replace("{top_k_positive_u2}", f"{self.html_stats.top_k_positive_u2}")
        self.html_txt = self.html_txt.replace("{top_k_negative_u1}", f"{self.html_stats.top_k_negative_u1}")
        self.html_txt = self.html_txt.replace("{top_k_negative_u2}", f"{self.html_stats.top_k_negative_u2}")
        # Emoji Ranking
        self.html_txt = self.html_txt.replace("{emoji1_u1}", f"{self.html_stats.emoji1_u1}")
        self.html_txt = self.html_txt.replace("{emoji1_u2}", f"{self.html_stats.emoji1_u2}")
        self.html_txt = self.html_txt.replace("{emoji2_u1}", f"{self.html_stats.emoji2_u1}")
        self.html_txt = self.html_txt.replace("{emoji2_u2}", f"{self.html_stats.emoji2_u2}")
        self.html_txt = self.html_txt.replace("{emoji3_u1}", f"{self.html_stats.emoji3_u1}")
        self.html_txt = self.html_txt.replace("{emoji3_u2}", f"{self.html_stats.emoji3_u2}")
        self.html_txt = self.html_txt.replace("{emoji4_u1}", f"{self.html_stats.emoji4_u1}")
        self.html_txt = self.html_txt.replace("{emoji4_u2}", f"{self.html_stats.emoji4_u2}")
        self.html_txt = self.html_txt.replace("{emoji5_u1}", f"{self.html_stats.emoji5_u1}")
        self.html_txt = self.html_txt.replace("{emoji5_u2}", f"{self.html_stats.emoji5_u2}")
        return self

    def populate_html_img(self):
        """

        :return:
        """
        self.html_txt = self.html_txt.replace("{word_cloud_1words_u1}", f"{self.html_images.word_cloud_1words_u1}")
        self.html_txt = self.html_txt.replace("{word_cloud_1words_u2}", f"{self.html_images.word_cloud_1words_u2}")
        self.html_txt = self.html_txt.replace("{word_cloud_2words_u1}", f"{self.html_images.word_cloud_2words_u1}")
        self.html_txt = self.html_txt.replace("{word_cloud_2words_u2}", f"{self.html_images.word_cloud_2words_u2}")
        self.html_txt = self.html_txt.replace("{word_cloud_3words_u1}", f"{self.html_images.word_cloud_3words_u1}")
        self.html_txt = self.html_txt.replace("{word_cloud_3words_u2}", f"{self.html_images.word_cloud_3words_u2}")

        self.html_txt = self.html_txt.replace("{date_n_msgs}", f"{self.html_images.date_n_msgs}")
        self.html_txt = self.html_txt.replace("{date_n_emojis}", f"{self.html_images.date_n_emojis}")
        self.html_txt = self.html_txt.replace("{weekly_pattern}", f"{self.html_images.weekly_pattern}")
        self.html_txt = self.html_txt.replace("{hourly_pattern}", f"{self.html_images.hourly_pattern}")
        self.html_txt = self.html_txt.replace("{monthly_msg_pattern}", f"{self.html_images.monthly_msg_pattern}")
        self.html_txt = self.html_txt.replace("{monthly_word_pattern}", f"{self.html_images.monthly_word_pattern}")
        self.html_txt = self.html_txt.replace("{monthly_emoji_pattern}", f"{self.html_images.monthly_emoji_pattern}")
        self.html_txt = self.html_txt.replace("{monthly_response_pattern}",
                                              f"{self.html_images.monthly_response_pattern}")
        self.html_txt = self.html_txt.replace("{monthly_first_text_ct}", f"{self.html_images.monthly_first_text_ct}")
        self.html_txt = self.html_txt.replace("{monthly_avg_polarity}", f"{self.html_images.monthly_avg_polarity}")
        self.html_txt = self.html_txt.replace("{domain_counts}", f"{self.html_images.domain_counts}")
        return self

    def save_html(self):
        """

        :return:
        """
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_name = f"chat_explore_{current_time}.html"
        with open(f'{self.file_name}', 'wb') as f:
            f.write(self.html_txt.encode('utf-8'))
        return self
