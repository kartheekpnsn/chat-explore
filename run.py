"""
    Acknowledgement:
    - This entire idea is inspired from a reddit post (links posted below):
    - Link: https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/
    - Author Citation: https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/eem8gke/

    ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐
    <================== This entire code is placed in: https://github.com/kartheekpnsn/chat-explore ==================>
    ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐(◣_◢)┌∩┐ ┌∩┐
"""
# Load System Modules --------------------------------------------------------------------------------------------------
import os
import sys
import warnings

warnings.filterwarnings('ignore')

sys.path.append(os.path.abspath(os.path.join('src/')))

# Load User defined Modules --------------------------------------------------------------------------------------------
from preprocess import Preprocess
from user import User
from action_logging import Logger
from plot_user import PlotUser
from plot import Plot
from plot_progression import PlotProgression
from generate_html import HTML
from delete_files import DeleteFiles

# Setup Logger ---------------------------------------------------------------------------------------------------------
logger = Logger(log_flag = True, log_file = "run", log_path = "logs/")

# Load and Clean the data ----------------------------------------------------------------------------------------------
preprocess = Preprocess(input_file = 'data/input-muzu.txt', logger = logger)
preprocess.read_file()
preprocess.clean_data()
preprocess.drop_message()
preprocess.prepare_df()
preprocess.check_n_users()

# Start Analysis -------------------------------------------------------------------------------------------------------
user_data_list = []
for user_idx, user in enumerate(preprocess.users + ['Overall']):
    logger.write_logger(f"Starting for User: {user}")
    if user == 'Overall':
        user_subset_data = preprocess.pd_data.copy()
    else:
        user_subset_data = preprocess.pd_data[preprocess.pd_data['User'] == user]

    # Fetch user statistics --------------------------------------------------------------------------------------------
    user_data = User(
        user_name = user,
        color_map = preprocess.color_map,
        messages = user_subset_data['Message'],
        timestamp = user_subset_data['Timestamp'],
        users = user_subset_data['User'],
        logger = logger)
    user_data.get_clean_messages(). \
        get_link_count(). \
        get_media_count(). \
        get_emoji_count(). \
        get_total_stats(). \
        get_emoji_statistics(). \
        get_avg_stats(). \
        get_top_stats(data = preprocess.pd_data). \
        get_response_time(data = preprocess.pd_data)

    # Plot user statistics ---------------------------------------------------------------------------------------------
    plot_user_obj = PlotUser(user_object = user_data, user_idx = user_idx + 1)
    plot_user_obj.plot_top_k_ngrams(n_grams = 1, k = 10)
    plot_user_obj.plot_top_k_ngrams(n_grams = 2, k = 10)
    plot_user_obj.plot_top_k_ngrams(n_grams = 3, k = 10)
    user_data.pd_emoji_rank = plot_user_obj.plot_top_k_emojis(k = 5, normalize = True)
    plot_user_obj.plot_word_cloud()
    plot_user_obj.plot_word_cloud(n_grams = 2)
    plot_user_obj.plot_word_cloud(n_grams = 3)

    user_data_list.append(user_data)

    logger.write_logger(f"Ending for User: {user}")

# Plot the Overall Stats -----------------------------------------------------------------------------------------------
plot_obj = Plot(data = preprocess.pd_data, color_map = preprocess.color_map)
plot_obj.plot_date_n_msgs()
plot_obj.plot_weekday_n_msgs()
plot_obj.plot_hour_n_msgs()
plot_obj.plot_domain_counts(user_object = user_data_list[-1])
plot_obj.plot_date_n_emojis(user_object = user_data_list[-1])
# TODO: Add body to the media count method
# plot_obj.plot_media_counts(user_object = user_data_list[-1])

# Plot the Progression -------------------------------------------------------------------------------------------------
plot_progression_obj = PlotProgression(data = preprocess.pd_data, color_map = preprocess.color_map)
plot_progression_obj.plot_monthly_msg_progression()
plot_progression_obj.plot_monthly_word_progression(user_object = user_data_list[-1])
plot_progression_obj.plot_monthly_emoji_progression(user_object = user_data_list[-1])
plot_progression_obj.plot_monthly_response_time_progression(user_object = user_data_list[-1])

# Generate HTML --------------------------------------------------------------------------------------------------------
html_obj = HTML(user1 = user_data_list[0], user2 = user_data_list[1], overall = user_data_list[2], logger = logger)
html_obj.populate_members().\
    populate_html_txt().\
    populate_html_img().\
    save_html()

# Delete Logs and Plots to save memory ---------------------------------------------------------------------------------
DeleteFiles(path_list = ('plots/', )).delete()