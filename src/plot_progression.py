import os
import warnings
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

warnings.filterwarnings('ignore')


class PlotProgression:

    def __init__(self, data = None, color_map = None, save_path = "../plots/"):
        """

        :param data:
        :param color_map:
        :param save_path:
        """
        self.data = data
        self.data['Month'] = self.data['Timestamp'].dt.strftime('(%Y) %m')
        self.color_map = color_map
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok = True)

    @staticmethod
    def get_trend_points(points):
        """

        :param x:
        :param y:
        :return:
        """

    def plot_monthly_msg_progression(self):
        """

        :return:
        """
        monthly_msg_progression = self.data.groupby(['Month', 'User'])['Message'].count().reset_index()
        monthly_msg_progression.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = '# of Msgs',
                         hue = 'User', hue_order = list(self.color_map.keys()),
                         palette = list(self.color_map.values()),
                         data = monthly_msg_progression, markers = True)
        plt.xticks(rotation = 90)
        g.set_xlabel('(Year) Month')
        plt.savefig(f"{self.save_path}/monthly_msg_progression.png", dpi = 300)

    def plot_monthly_word_progression(self, user_object):
        """

        :return:
        """
        monthly_word_progression = user_object.get_userwise_monthly_word_counts()
        monthly_word_progression.rename(columns = {'Word Count': 'Avg. # of Words (per Msg)'}, inplace = True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = 'Avg. # of Words (per Msg)',
                         hue = 'User', hue_order = list(self.color_map.keys()),
                         palette = list(self.color_map.values()),
                         data = monthly_word_progression, markers = True)
        plt.xticks(rotation = 90)
        g.set_xlabel('(Year) Month')
        plt.savefig(f"{self.save_path}/monthly_word_progression.png", dpi = 300)

    def plot_monthly_response_time_progression(self, user_object):
        """

        :return:
        """
        monthly_response_time_progression = user_object.get_userwise_monthly_response_time(data = self.data)
        monthly_response_time_progression.rename(columns = {'Response (Min)': 'Avg. Response (Min)'}, inplace = True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = 'Avg. Response (Min)',
                         hue = 'User', hue_order = list(self.color_map.keys()),
                         palette = list(self.color_map.values()),
                         data = monthly_response_time_progression, markers = True)
        plt.xticks(rotation = 90)
        g.set_xlabel('(Year) Month')
        plt.savefig(f"{self.save_path}/monthly_response_time_progression.png", dpi = 300)

    def plot_monthly_emoji_progression(self, user_object):
        """

        :return:
        """
        monthly_emoji_progression = user_object.get_userwise_monthly_emoji_counts()
        monthly_emoji_progression.rename(columns = {'Emoji Count': 'Avg. # of Emojis (per Msg)'}, inplace = True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = 'Avg. # of Emojis (per Msg)',
                         hue = 'User', hue_order = list(self.color_map.keys()),
                         palette = list(self.color_map.values()),
                         data = monthly_emoji_progression, markers = True)
        plt.xticks(rotation = 90)
        g.set_xlabel('(Year) Month')
        plt.savefig(f"{self.save_path}/monthly_emoji_progression.png", dpi = 300)
