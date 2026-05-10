import os
import warnings

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

warnings.filterwarnings("ignore")


class PlotUser:
    def __init__(
        self, store=None, user_idx=1, user_color="#2ecc71", save_path="plots/"
    ):
        self.store = store
        self.user_idx = user_idx
        self.user_color = user_color
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def plot_top_k_ngrams(self, n_grams=1, k=10):
        top_k_words = self.store.load_df(f"top_k_{n_grams}words_u{self.user_idx}")
        plt.figure(figsize=(12, 7))
        g = sns.barplot(x="Word", y="Count", data=top_k_words, color=self.user_color)
        g.set_xticklabels(g.get_xticklabels(), rotation=90)
        g.set_xlabel("Word", size=12, fontdict={"fontweight": "bold"})
        g.set_ylabel("Count", size=12, fontdict={"fontweight": "bold"})
        plt.savefig(
            f"{self.save_path}/top_{k}_{n_grams}words_u{self.user_idx}.png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0,
        )

    def plot_word_cloud(self, n_grams=1):
        words = self.store.load_json(f"word_cloud_{n_grams}words_u{self.user_idx}")
        wordcloud_words = " ".join(words)
        if self.user_color == "#3498db":
            colormap = "Blues"
        elif self.user_color == "#2ecc71":
            colormap = "Greens"
        else:
            colormap = "Reds"
        wordcloud = WordCloud(
            width=500,
            height=800,
            colormap=colormap,
            background_color="white",
            collocations=False,
            min_font_size=10,
        ).generate(wordcloud_words)
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(
            f"{self.save_path}/word_cloud_{n_grams}words_u{self.user_idx}.png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0,
        )

    def plot_top_k_emojis(self, k=10):
        top_k_emojis = self.store.load_df(f"top_k_emojis_u{self.user_idx}")
        return top_k_emojis
