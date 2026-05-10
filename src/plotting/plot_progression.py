import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


class PlotProgression:

    def __init__(self, store=None, color_map=None, min_year=None, max_year=None,
                 max_years=3, cumulative=False, save_path="plots/"):
        self.store = store
        self.color_map = color_map
        self.cumulative = cumulative
        self.save_path = save_path

        if max_years is not None:
            if (max_year - min_year) < max_years:
                max_years = max_year - min_year
            min_year = max_year - max_years

        self.month_df = PlotProgression.prepare_month_df(min_year, max_year)
        os.makedirs(self.save_path, exist_ok=True)

    @staticmethod
    def prepare_month_df(min_year, max_year):
        months = []
        for year in range(min_year, (max_year + 1)):
            for month in range(1, 13):
                months.append(f"({year}) {month:02d}")
        return pd.DataFrame({'Month': months})

    def _plot_monthly(self, df, y, filename):
        fig = plt.figure(figsize=(15, 7))
        plt.grid(True)
        ax = fig.add_subplot(111)
        g = None
        for each_user in np.unique(df['User']):
            subset = df[df['User'] == each_user].copy()
            subset = subset.sort_values(['Month'], ascending=True)
            subset = self.month_df.merge(subset, on='Month', how='left')
            subset['User'] = subset['User'].fillna(each_user)
            subset[y] = subset[y].fillna(0)
            if self.cumulative:
                subset[y] = subset[y].cumsum()
            g = sns.lineplot(x='Month', y=y,
                             data=subset, color=self.color_map[each_user],
                             label=each_user, sort=False, ax=ax)
        if g is not None:
            g.set_xlabel('(Year) Month', size=12, fontdict={'fontweight': 'bold'})
            g.set_ylabel(y, size=12, fontdict={'fontweight': 'bold'})
        ax.legend()
        plt.xticks(rotation=90)
        plt.savefig(f"{self.save_path}/{filename}.png", dpi=300, bbox_inches='tight', pad_inches=0)

    def plot_monthly_msg_progression(self):
        df = self.store.load_df("monthly_msg_progression")
        self._plot_monthly(df, "# of Msgs", "monthly_msg_progression")

    def plot_monthly_word_progression(self):
        df = self.store.load_df("monthly_word_progression")
        self._plot_monthly(df, "Avg. # of Words (per Msg)", "monthly_word_progression")

    def plot_monthly_emoji_progression(self):
        df = self.store.load_df("monthly_emoji_progression")
        self._plot_monthly(df, "Avg. # of Emojis (per Msg)", "monthly_emoji_progression")

    def plot_first_text_progression(self):
        df = self.store.load_df("monthly_first_text_ct")
        self._plot_monthly(df, "No. of times user texted first", "monthly_first_text_ct")

    def plot_sentiment_progression(self):
        df = self.store.load_df("monthly_avg_polarity")
        self._plot_monthly(df, "Avg. Mood Score", "monthly_avg_polarity")

    def plot_monthly_response_time_progression(self):
        df = self.store.load_df("monthly_response_time_progression")
        self._plot_monthly(df, "Avg. Response (Min)", "monthly_response_time_progression")
