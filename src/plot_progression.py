import os
import warnings

import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class PlotProgression:

    def __init__(self, data = None, color_map = None, save_path = "plots/"):
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
        pass

    def plot_monthly_msg_progression(self):
        """

        :return:
        """
        monthly_msg_progression = self.data.groupby(['Month', 'User'])['Message'].count().reset_index()
        monthly_msg_progression.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        monthly_msg_progression.sort_values(['User','Month'], inplace=True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        g = sns.lineplot(x = 'Month', y = '# of Msgs',
                         hue = 'User', hue_order = hue_order,
                         palette = palette, sort=False,
                         data = monthly_msg_progression)
        plt.xticks(rotation = 90)
        # g.set_title(f"Trend in Number of msgs sent", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"# of Msgs", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/monthly_msg_progression.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_monthly_word_progression(self, user_object):
        """

        :return:
        """
        monthly_word_progression = user_object.get_userwise_monthly_word_counts()
        monthly_word_progression.rename(columns = {'Word Count': 'Avg. # of Words (per Msg)'}, inplace = True)
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        g = sns.lineplot(x = 'Month', y = 'Avg. # of Words (per Msg)',
                         hue = 'User', hue_order = hue_order,
                         palette = palette,
                         data = monthly_word_progression, markers = True)
        plt.xticks(rotation = 90)
        # g.set_title(f"Trend in Average Number of Words used per msg", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"Avg. # of Words (per Msg)", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/monthly_word_progression.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_monthly_response_time_progression(self, user_object):
        """

        :return:
        """
        monthly_response_time_progression = user_object.get_userwise_monthly_response_time(data = self.data)
        monthly_response_time_progression.rename(columns = {'Response (Min)': 'Avg. Response (Min)'}, inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = 'Avg. Response (Min)',
                         hue = 'User', hue_order = hue_order,
                         palette = palette,
                         data = monthly_response_time_progression, markers = True)
        plt.xticks(rotation = 90)
        # g.set_title(f"Trend in Avg. Response time", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"Avg. Response (Min)", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/monthly_response_time_progression.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_monthly_emoji_progression(self, user_object):
        """

        :return:
        """
        monthly_emoji_progression = user_object.get_userwise_monthly_emoji_counts()
        monthly_emoji_progression.rename(columns = {'Emoji Count': 'Avg. # of Emojis (per Msg)'}, inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Month', y = 'Avg. # of Emojis (per Msg)',
                         hue = 'User', hue_order = hue_order,
                         palette = palette,
                         data = monthly_emoji_progression, markers = True)
        plt.xticks(rotation = 90)
        # g.set_title(f"Trend in Avg. Emojis sent per msg", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"Avg. # of Emojis (per Msg)", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/monthly_emoji_progression.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)
