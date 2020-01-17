import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class PlotProgression:

    def __init__(self, data = None, max_years = 3, color_map = None, cumulative = False, save_path = "plots/"):
        """

        :param data:
        :param max_years:
        :param color_map:
        :param save_path:
        """
        self.data = data
        self.data['Month'] = self.data['Timestamp'].dt.strftime('(%Y) %m')
        self.max_years = max_years
        self.color_map = color_map
        self.save_path = save_path
        self.cumulative = cumulative
        min_year = min(self.data['Timestamp'].dt.year)
        max_year = max(self.data['Timestamp'].dt.year)
        if self.max_years is not None:
            if (max_year - min_year) < self.max_years:
                self.max_years = max_year - min_year
            min_year = (max_year - self.max_years)
        self.month_df = PlotProgression.prepare_month_df(min_year, max_year)
        os.makedirs(self.save_path, exist_ok = True)

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
        y = "# of Msgs"
        monthly_msg_progression = self.data.groupby(['Month', 'User'])['Message'].count().reset_index()
        monthly_msg_progression.rename(columns = {'Message': y}, inplace = True)
        monthly_msg_progression.sort_values(['User', 'Month'], inplace = True)
        fig = plt.figure(figsize = (15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(monthly_msg_progression['User']):
            subset_plot_data = monthly_msg_progression[monthly_msg_progression['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user, sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Number of msgs sent", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_msg_progression.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)

    def plot_monthly_word_progression(self, user_object):
        """

        :return:
        """
        y = "Avg. # of Words (per Msg)"
        monthly_word_progression = user_object.get_userwise_monthly_word_counts()
        monthly_word_progression.rename(columns = {'Word Count': y}, inplace = True)
        fig = plt.figure(figsize = (15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(monthly_word_progression['User']):
            subset_plot_data = monthly_word_progression[monthly_word_progression['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user, sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Average Number of Words used per msg", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_word_progression.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)

    def plot_monthly_response_time_progression(self, user_object):
        """

        :return:
        """
        y = 'Avg. Response (Min)'
        monthly_response_time_progression = user_object.get_userwise_monthly_response_time(data = self.data)
        monthly_response_time_progression.rename(columns = {'Response (Min)': y}, inplace = True)
        fig = plt.figure(figsize = (15, 7))
        ax = fig.add_subplot(111)
        plt.grid(True)
        g = None
        for each_user in np.unique(monthly_response_time_progression['User']):
            subset_plot_data = monthly_response_time_progression[monthly_response_time_progression['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user, sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Avg. Response time", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_response_time_progression.png", dpi = 300, bbox_inches = 'tight',
                    pad_inches = 0)

    def plot_first_text_progression(self, user_object):
        """

        :param user_object:
        :return:
        """
        y = 'No. of times user texted first'
        monthly_first_text_ct = user_object.get_first_text_monthly_count()
        monthly_first_text_ct.rename(columns = {'Date': y}, inplace = True)
        fig = plt.figure(figsize = (15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(monthly_first_text_ct['User']):
            subset_plot_data = monthly_first_text_ct[monthly_first_text_ct['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user,
                             sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Avg. Emojis sent per msg", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_first_text_ct.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)

    def plot_sentiment_progression(self, user_object):
        """

        :param user_object:
        :return:
        """
        y = 'Avg. Mood Score'
        monthly_avg_polarity = user_object.get_monthly_avg_polarity()
        monthly_avg_polarity.rename(columns = {'Polarity Score': y}, inplace = True)
        fig = plt.figure(figsize = (15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(monthly_avg_polarity['User']):
            subset_plot_data = monthly_avg_polarity[monthly_avg_polarity['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user,
                             sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Avg. Emojis sent per msg", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_avg_polarity.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)

    def plot_monthly_emoji_progression(self, user_object):
        """

        :return:
        """
        y = 'Avg. # of Emojis (per Msg)'
        monthly_emoji_progression = user_object.get_userwise_monthly_emoji_counts()
        monthly_emoji_progression.rename(columns = {'Emoji Count': y}, inplace = True)
        fig = plt.figure(figsize = (15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(monthly_emoji_progression['User']):
            subset_plot_data = monthly_emoji_progression[monthly_emoji_progression['User'] == each_user]
            subset_plot_data = subset_plot_data.sort_values(['Month'], ascending = True)
            subset_plot_data = self.month_df.merge(subset_plot_data, on = 'Month', how = 'left')
            subset_plot_data['User'] = subset_plot_data['User'].fillna(each_user)
            subset_plot_data[y] = subset_plot_data[y].fillna(0)
            if self.cumulative:
                subset_plot_data[y] = subset_plot_data[y].cumsum()
            g = sns.lineplot(x = 'Month', y = y,
                             data = subset_plot_data, color = self.color_map[each_user],
                             label = each_user,
                             sort = False, ax = ax)
        if g is not None:
            # g.set_title(f"Trend in Avg. Emojis sent per msg", size = 20, fontdict = {'fontweight': 'bold'})
            g.set_xlabel('(Year) Month', size = 12, fontdict = {'fontweight': 'bold'})
            g.set_ylabel(f"{y}", size = 12, fontdict = {'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation = 90)
        plt.savefig(f"{self.save_path}/monthly_emoji_progression.png", dpi = 300, bbox_inches = 'tight', pad_inches = 0)
