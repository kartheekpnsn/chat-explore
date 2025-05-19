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
import pickle
import sys
import warnings
import webbrowser
from argparse import ArgumentParser, RawTextHelpFormatter

import tqdm

warnings.filterwarnings("ignore")

sys.path.append(os.path.abspath(os.path.join("src/")))

from action_logging import Logger
from delete_files import DeleteFiles
from generate_html import HTML
from llm import OpenAIUtils
from plot import Plot
from plot_progression import PlotProgression
from plot_user import PlotUser
from preprocess import Preprocess
from user import User

# Load User defined Modules --------------------------------------------------------------------------------------------
from utils import isTextBasedBrowser


# Methods to be run ----------------------------------------------------------------------------------------------------
def preprocess_data(filePath, logger):
    """
    Remove the below messages
    - (Encryption, Security code, Missed group/voice/video calls, live locations, Attached contacts)
    :param filePath:
    :param logger:
    :return:
    """
    # Load and Clean the data ------------------------------------------------------------------------------------------
    preprocess = Preprocess(input_file=filePath, logger=logger)
    preprocess.read_file()
    preprocess.drop_message().drop_message(
        contains="security code changed"
    ).drop_message(contains="Missed group voice call").drop_message(
        contains="Missed voice call"
    ).drop_message(
        contains="Missed video call"
    ).drop_message(
        contains="Missed group video call"
    ).drop_message(
        contains="live location shared"
    ).drop_message(
        contains=".vcf (file attached)"
    )
    preprocess.clean_data(True)
    preprocess.prepare_df()
    preprocess.check_n_users()
    preprocess.remove_forward_messages(min_length=15)
    preprocess.write_data()
    return preprocess


if __name__ == "__main__":
    # Setup Logger -----------------------------------------------------------------------------------------------------
    logger = Logger(log_flag=True, log_file="run", log_path="logs/")

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", dest="file", help="Option to load the file.")

    args = parser.parse_args()
    filePath = args.file

    # Preprocess the data ----------------------------------------------------------------------------------------------
    preprocess = preprocess_data(filePath, logger)
