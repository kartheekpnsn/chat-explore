import os
import warnings
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

warnings.filterwarnings('ignore')


class Plot:

    def __init__(self, data = None, color_map = None, save_path = "plots/"):
        """

        :param data:
        :param save_path:
        """
        self.data = data
        self.color_map = color_map
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok = True)

    @staticmethod
    def formulate_date_df(start_date, end_date):
        """

        :param start_date:
        :param end_date:
        :return:
        """
        return pd.DataFrame({'Date': pd.date_range(start = start_date, end = end_date)})

    def plot_date_n_msgs(self):
        """

        :return:
        """
        date_n_msgs = self.data.groupby(['Date', 'User'])['Message'].count().reset_index()
        date_n_msgs['Date'] = pd.to_datetime(date_n_msgs['Date'], format = '%d-%b-%Y')
        date_n_msgs.sort_values('Date', inplace = True)
        full_date_df = Plot.formulate_date_df(start_date = min(date_n_msgs['Date']),
                                              end_date = max(date_n_msgs['Date']))
        date_n_msgs = full_date_df.merge(date_n_msgs, on = 'Date', how = 'left')
        date_n_msgs['Message'] = date_n_msgs['Message'].fillna(0)
        date_n_msgs.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        date_n_msgs.sort_values(['User', 'Date'], inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Date', y = '# of Msgs',
                         hue = 'User', hue_order = hue_order,
                         palette = palette,
                         data = date_n_msgs, markers = True)
        # g.set_title(f"# of Msgs sent over time", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('Date', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"# of Msgs", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/date_n_msgs.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_weekday_n_msgs(self):
        """

        :return:
        """
        weekday_n_msgs = self.data.groupby(['Weekday', 'User'])['Message'].count().reset_index()
        full_weekday_df = pd.DataFrame({
            'Weekday': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        })
        weekday_n_msgs = full_weekday_df.merge(weekday_n_msgs, on = 'Weekday', how = 'left')
        weekday_n_msgs['Message'] = weekday_n_msgs['Message'].fillna(0)
        weekday_n_msgs.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.barplot(x = 'Weekday', y = '# of Msgs',
                        hue = 'User', hue_order = hue_order,
                        palette = palette,
                        data = weekday_n_msgs)
        # g.set_title(f"Weekday Texting Pattern", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('Weekday', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"# of Msgs", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/weekday_n_msgs.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_hour_n_msgs(self):
        """

        :return:
        """
        self.data['Hour'] = self.data['Timestamp'].dt.hour
        hour_n_msgs = self.data.groupby(['Hour', 'User'])['Message'].count().reset_index()
        full_hour_df = pd.DataFrame({
            'Hour': np.arange(24)
        })
        hour_n_msgs = full_hour_df.merge(hour_n_msgs, on = 'Hour', how = 'left')
        hour_n_msgs['Message'] = hour_n_msgs['Message'].fillna(0)
        hour_n_msgs.rename(columns = {'Message': '# of Msgs'}, inplace = True)
        hour_n_msgs.sort_values(['User', 'Hour'], inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        # plt.grid(True)
        g = sns.barplot(x = 'Hour', y = '# of Msgs',
                        hue = 'User', hue_order = hue_order,
                        palette = palette,
                        data = hour_n_msgs)
        # g.set_title(f"Hourly Texting Pattern", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('Hour', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"# of Msgs", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/hour_n_msgs.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)

    def plot_date_n_emojis(self, user_object):
        """

        :return:
        """
        date_n_emojis = user_object.get_userwise_emoji_count()
        date_n_emojis['Date'] = pd.to_datetime(date_n_emojis['Date'], format = '%d-%b-%Y')
        date_n_emojis.sort_values('Date', inplace = True)
        full_date_df = Plot.formulate_date_df(start_date = min(date_n_emojis['Date']),
                                              end_date = max(date_n_emojis['Date']))
        date_n_emojis = full_date_df.merge(date_n_emojis, on = 'Date', how = 'left')
        date_n_emojis['Emoji Count'] = date_n_emojis['Emoji Count'].fillna(0)
        date_n_emojis.rename(columns = {'Emoji Count': '# of Emojis'}, inplace = True)
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        g = sns.lineplot(x = 'Date', y = '# of Emojis',
                         hue = 'User', hue_order = hue_order,
                         palette = palette,
                         data = date_n_emojis, markers = True)
        # g.set_title(f"Emojis sent over time", size = 20, fontdict = {'fontweight': 'bold'})
        g.set_xlabel('Date', size = 12, fontdict = {'fontweight': 'bold'})
        g.set_ylabel(f"# of Emojis", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/date_n_emojis.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)

    def plot_media_counts(self, user_object):
        """

        :param user_object:
        :return:
        """
        #TODO: Add this media count
        pass

    def plot_domain_counts(self, user_object):
        """

        :return:
        """
        domain_counts = user_object.get_domain_count()
        hue_order = sorted(list(self.color_map.keys()))
        palette = [self.color_map[v] for v in hue_order]
        plt.figure(figsize = (15, 7))
        plt.grid(True)
        if domain_counts.shape[0] > 0:
            g = sns.barplot(x = 'Domain', y = 'Count',
                            hue = 'User', hue_order = hue_order,
                            palette = palette,
                            data = domain_counts)
            g.set_xticklabels(g.get_xticklabels(), rotation = 90)
            g.set_ylabel('Count', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_xlabel(f"Domain of the link shared", size = 12, fontdict = {'fontweight': 'bold'})
        plt.savefig(f"{self.save_path}/domain_counts.png", dpi = 300, bbox_inches = 'tight',pad_inches = 0)
