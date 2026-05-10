"""
Acknowledgement:
- This entire idea is inspired from a reddit post (links posted below):
- Link: https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/
- Author Citation: https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/eem8gke/

┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐
<== https://github.com/kartheekpnsn/chat-explore ==>
┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐
"""

# Load System Modules --------------------------------------------------------------------------------------------------  # noqa: E501
import os
import sys
import warnings
import webbrowser
from argparse import ArgumentParser, RawTextHelpFormatter

warnings.filterwarnings("ignore")

from src.core.preprocess import Preprocess  # noqa: E402
from src.core.user import User  # noqa: E402
from src.output.generate_html import HTML  # noqa: E402
from src.plotting.plot import Plot  # noqa: E402
from src.plotting.plot_progression import PlotProgression  # noqa: E402
from src.plotting.plot_user import PlotUser  # noqa: E402
from src.utils.action_logging import Logger  # noqa: E402
from src.utils.delete_files import DeleteFiles  # noqa: E402
from src.utils.helpers import isTextBasedBrowser  # noqa: E402
from src.utils.metrics_store import MetricsStore  # noqa: E402


# Methods to be run ----------------------------------------------------------------------------------------------------  # noqa: E501
def preprocess_data(filePath, logger):
    """
    Remove the below messages
    - (Encryption, Security code, Missed group/voice/video calls,
       live locations, Attached contacts)
    :param filePath:
    :param logger:
    :return:
    """
    # Load and Clean the data ------------------------------------------------------------------------------------------  # noqa: E501
    preprocess = Preprocess(input_file=filePath, logger=logger)
    preprocess.read_file()
    preprocess.drop_message().drop_message(
        contains="security code changed"
    ).drop_message(contains="Messages and calls are end").drop_message(
        contains="Your security code with"
    ).drop_message(contains="Missed group voice call").drop_message(
        contains="Missed voice call"
    ).drop_message(contains="Missed video call").drop_message(
        contains="Missed group video call"
    ).drop_message(contains="live location shared").drop_message(
        contains=".vcf (file attached)"
    )
    preprocess.prepare_df()
    preprocess.check_n_users()
    preprocess.remove_forward_messages(min_length=15)
    preprocess.write_data()
    return preprocess


def user_wise_analysis(preprocess, logger):
    """

    :param preprocess:
    :param logger:
    :return:
    """
    # Start Analysis ---------------------------------------------------------------------------------------------------  # noqa: E501
    user_data_list = []
    for _, user in enumerate(preprocess.users + ["Overall"]):
        logger.write_logger(f"Starting for User: {user}")
        if user == "Overall":
            user_subset_data = preprocess.pd_data.copy()
        else:
            user_subset_data = preprocess.pd_data[preprocess.pd_data["User"] == user]

        # Fetch user statistics ----------------------------------------------------------------------------------------  # noqa: E501
        user_data = User(
            user_name=user,
            color_map=preprocess.color_map,
            messages=user_subset_data["Message"],
            timestamp=user_subset_data["Timestamp"],
            users=user_subset_data["User"],
            logger=logger,
        )
        user_data.get_clean_messages().get_message_sentiment().get_top_sentiments(
            k=2
        ).get_link_count().get_media_count().get_emoji_count().get_total_stats().get_emoji_statistics().get_avg_stats().get_top_stats(
            data=preprocess.pd_data
        ).get_response_time(data=preprocess.pd_data)

        user_data_list.append(user_data)

        logger.write_logger(f"Ending for User: {user}")
    return user_data_list


def plot_user_wise(store, user_data_list):
    """

    :param store:
    :param user_data_list:
    :return:
    """
    meta = store.load_json("meta")
    for user_idx, user_data in enumerate(user_data_list):
        u = user_idx + 1
        plot_user_obj = PlotUser(
            store=store,
            user_idx=u,
            user_color=meta["user_colors"][user_data.user_name],
        )
        plot_user_obj.plot_top_k_ngrams(n_grams=1, k=10)
        plot_user_obj.plot_top_k_ngrams(n_grams=2, k=10)
        plot_user_obj.plot_top_k_ngrams(n_grams=3, k=10)
        user_data.pd_emoji_rank = plot_user_obj.plot_top_k_emojis(k=5)
        plot_user_obj.plot_word_cloud(n_grams=1)
        plot_user_obj.plot_word_cloud(n_grams=2)
        plot_user_obj.plot_word_cloud(n_grams=3)


def save_metrics(preprocess, user_data_list, store):
    """
    Compute all plot metrics and persist them as JSON in data/json/.

    :param preprocess:
    :param user_data_list:
    :param store: MetricsStore instance
    :return:
    """
    import numpy as np
    import pandas as pd

    data = preprocess.pd_data
    overall = user_data_list[-1]

    # --- overall plots ---
    date_n_msgs = data.groupby(["Date", "User"])["Message"].count().reset_index()
    date_n_msgs["Date"] = pd.to_datetime(date_n_msgs["Date"], format="%d-%b-%Y")
    date_n_msgs.sort_values("Date", inplace=True)
    date_n_msgs["Date"] = date_n_msgs["Date"].dt.strftime("%d-%b-%Y")
    date_n_msgs.rename(columns={"Message": "# of Msgs"}, inplace=True)
    store.save_df("date_n_msgs", date_n_msgs)

    weekday_n_msgs = data.groupby(["Weekday", "User"])["Message"].count().reset_index()
    weekday_n_msgs.rename(columns={"Message": "# of Msgs"}, inplace=True)
    store.save_df("weekday_n_msgs", weekday_n_msgs)

    _tmp = data.copy()
    _tmp["Hour"] = _tmp["Timestamp"].dt.hour
    hour_n_msgs = _tmp.groupby(["Hour", "User"])["Message"].count().reset_index()
    hour_n_msgs.rename(columns={"Message": "# of Msgs"}, inplace=True)
    store.save_df("hour_n_msgs", hour_n_msgs)

    store.save_df("date_n_emojis", overall.get_userwise_emoji_count())
    store.save_df("domain_counts", overall.get_domain_count())

    # --- monthly progression ---
    _tmp2 = data.copy()
    _tmp2["Month"] = _tmp2["Timestamp"].dt.strftime("(%Y) %m")
    monthly_msg = _tmp2.groupby(["Month", "User"])["Message"].count().reset_index()
    monthly_msg.rename(columns={"Message": "# of Msgs"}, inplace=True)
    store.save_df("monthly_msg_progression", monthly_msg)

    monthly_word = overall.get_userwise_monthly_word_counts()
    monthly_word.rename(
        columns={"Word Count": "Avg. # of Words (per Msg)"}, inplace=True
    )
    store.save_df("monthly_word_progression", monthly_word)

    monthly_emoji = overall.get_userwise_monthly_emoji_counts()
    monthly_emoji.rename(
        columns={"Emoji Count": "Avg. # of Emojis (per Msg)"}, inplace=True
    )
    store.save_df("monthly_emoji_progression", monthly_emoji)

    monthly_first_text = overall.get_first_text_monthly_count()
    monthly_first_text.rename(
        columns={"Date": "No. of times user texted first"}, inplace=True
    )
    store.save_df("monthly_first_text_ct", monthly_first_text)

    monthly_polarity = overall.get_monthly_avg_polarity()
    monthly_polarity.rename(columns={"Polarity Score": "Avg. Mood Score"}, inplace=True)
    store.save_df("monthly_avg_polarity", monthly_polarity)

    monthly_response = overall.get_userwise_monthly_response_time(data=data)
    monthly_response.rename(
        columns={"Response (Min)": "Avg. Response (Min)"}, inplace=True
    )
    store.save_df("monthly_response_time_progression", monthly_response)

    # --- per-user data ---
    for user_idx, user_data in enumerate(user_data_list):
        u = user_idx + 1
        store.save_df(
            f"top_k_1words_u{u}",
            user_data.get_top_k_words(n_grams=1, k=10, normalize=False),
        )
        store.save_df(
            f"top_k_2words_u{u}",
            user_data.get_top_k_words(n_grams=2, k=10, normalize=False),
        )
        store.save_df(
            f"top_k_3words_u{u}",
            user_data.get_top_k_words(n_grams=3, k=10, normalize=False),
        )
        top_emojis = user_data.get_top_k_emojis(k=5, normalize=True)
        top_emojis["Count %"] = np.round(top_emojis["Count"] * 100)
        store.save_df(f"top_k_emojis_u{u}", top_emojis)
        store.save_json(
            f"word_cloud_1words_u{u}", user_data.get_words_for_wordcloud(n_grams=1)
        )
        store.save_json(
            f"word_cloud_2words_u{u}", user_data.get_words_for_wordcloud(n_grams=2)
        )
        store.save_json(
            f"word_cloud_3words_u{u}", user_data.get_words_for_wordcloud(n_grams=3)
        )

    # --- metadata ---
    store.save_json(
        "meta",
        {
            "color_map": preprocess.color_map,
            "min_year": int(min(data["Timestamp"].dt.year)),
            "max_year": int(max(data["Timestamp"].dt.year)),
            "user_colors": {ud.user_name: ud.user_color for ud in user_data_list},
        },
    )


def plot_overall(store):
    """

    :param store:
    :return:
    """
    meta = store.load_json("meta")
    plot_obj = Plot(store=store, color_map=meta["color_map"])
    plot_obj.plot_date_n_msgs()
    plot_obj.plot_weekday_n_msgs()
    plot_obj.plot_hour_n_msgs()
    plot_obj.plot_domain_counts()
    plot_obj.plot_date_n_emojis()
    # TODO: Add body to the media count method
    # plot_obj.plot_media_counts()


def plot_progression(store):
    """

    :param store:
    :return:
    """
    meta = store.load_json("meta")
    plot_progression_obj = PlotProgression(
        store=store,
        color_map=meta["color_map"],
        min_year=meta["min_year"],
        max_year=meta["max_year"],
        cumulative=False,
    )
    plot_progression_obj.plot_monthly_msg_progression()
    plot_progression_obj.plot_monthly_word_progression()
    plot_progression_obj.plot_monthly_emoji_progression()
    plot_progression_obj.plot_first_text_progression()
    plot_progression_obj.plot_sentiment_progression()
    plot_progression_obj.plot_monthly_response_time_progression()


def generate_html(user_data_list, logger):
    """

    :param user_data_list:
    :param logger:
    :return:
    """
    html_obj = HTML(
        user1=user_data_list[0],
        user2=user_data_list[1],
        overall=user_data_list[2],
        logger=logger,
    )
    html_obj.populate_members().populate_html_txt().populate_html_img().save_html()
    return html_obj.file_name


if __name__ == "__main__":
    # Setup Logger
    logger = Logger(log_flag=True, log_file="run", log_path="logs/")

    # Load command line arguments
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="Path to the WhatsApp chat export .txt file.",
        required=True,
    )

    args = parser.parse_args()
    filePath = args.file

    if not os.path.exists(filePath):
        print(f"Error: file not found: {filePath}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(filePath):
        print(f"Error: not a file: {filePath}", file=sys.stderr)
        sys.exit(1)

    if os.path.getsize(filePath) == 0:
        print(f"Error: file is empty: {filePath}", file=sys.stderr)
        sys.exit(1)

    # Preprocess the data
    preprocess = preprocess_data(filePath, logger)

    # User wise Analysis
    user_data_list = user_wise_analysis(preprocess, logger)

    # Save all computed metrics to data/json/
    store = MetricsStore(path="data/json/")
    save_metrics(preprocess, user_data_list, store)

    # Plot user-wise Stats from JSON
    plot_user_wise(store, user_data_list)

    # Plot the Overall Stats from JSON
    plot_overall(store)

    # Plot the Progression from JSON
    plot_progression(store)

    # Generate HTML
    output_file = generate_html(user_data_list, logger)

    # Delete Logs and Plots to save memory
    DeleteFiles(path_list=("plots/", "logs/")).delete()

    # Open in browser
    if not isTextBasedBrowser(webbrowser.get()):
        try:
            logger.write_logger(f"Opening {output_file} in browser.")
            webbrowser.open("file://" + os.path.realpath(output_file))
        except webbrowser.Error:
            logger.write_logger(
                f"No runnable browser found. Open {output_file} manually."
            )
            logger.write_logger(
                f'Path to heatmap file: "{os.path.abspath(output_file)}"'
            )
