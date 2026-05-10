import os
import sys
import warnings

import pandas as pd

from src.core.parser import ChatParser, ParseError
from src.utils.action_logging import Logger

warnings.filterwarnings("ignore")


class Preprocess:

    def __init__(self, input_file, logger=None):
        self.file = input_file
        if logger is None:
            self.logger = Logger(
                log_flag=True, log_file="preprocess", log_path="../logs/"
            )
        else:
            self.logger = logger
        self.users = None
        self.color_map = {}
        self.data = None
        self.data_backup = None
        self.pd_data = None

    def read_file(self):
        self.logger.write_logger(
            "In preprocess.py (read_file): Reading of input file: "
            + self.file
            + " starts"
        )
        with open(self.file, "r", encoding="utf8") as f:
            self.data = f.read()
        self.data = self.data.splitlines()
        self.data_backup = self.data.copy()
        self.logger.write_logger(
            "In preprocess.py (read_file): Reading of input file: "
            + self.file
            + " ends"
        )

    def print_sample(self, n_lines=10):
        self.logger.write_logger(
            "In preprocess.py (print_sample): Printing first " + str(n_lines) + " lines"
        )
        print(self.data[:n_lines])

    def drop_message(
        self,
        contains="Messages to this chat and calls are now secured with end-to-end encryption",
    ):
        self.logger.write_logger(
            "In preprocess.py (drop_message): Dropping messages containing: " + contains
        )
        self.data = [line for line in self.data if contains not in line]
        return self

    def prepare_df(self):
        self.logger.write_logger(
            "In preprocess.py (prepare_df): Preparation of data frame starts"
        )
        try:
            parser = ChatParser(self.file)
            if self.data is not None:
                self.pd_data = parser.parse_lines(self.data)
            else:
                self.pd_data = parser.parse()
            self.users = list(self.pd_data["User"].unique())
        except ParseError as exc:
            self.logger.write_logger(
                f"In preprocess.py (prepare_df): {exc}", error=True
            )
            sys.exit(1)
        self.logger.write_logger(
            "In preprocess.py (prepare_df): Preparation of data frame ends"
        )

    def check_n_users(self):
        users = list(set(self.pd_data["User"].tolist()))
        n_users = len(users)
        if n_users != 2:
            self.logger.write_logger(
                "In preprocess.py (check_n_users): You need exactly 2 users in the chat.",
                error=True,
            )
            self.logger.write_logger(
                f"In preprocess.py (check_n_users): Found {n_users} users: {','.join(users)}",
                error=True,
            )
            sys.exit(1)
        else:
            self.color_map = {
                self.users[0]: "#e74c3c",
                self.users[1]: "#3498db",
            }
            self.logger.write_logger(
                "In preprocess.py (check_n_users): 2 users confirmed.", error=False
            )

    def remove_forward_messages(self, min_length=15):
        message_count = (
            self.pd_data.groupby(["User", "Timestamp"])["Message"].count().reset_index()
        )
        messages_to_remove = message_count[message_count["Message"] > min_length][
            ["User", "Timestamp"]
        ]
        messages_to_remove = messages_to_remove.copy()
        messages_to_remove["Is Forward"] = True
        self.pd_data = self.pd_data.merge(
            messages_to_remove, on=["User", "Timestamp"], how="left"
        )
        self.pd_data["Is Forward"] = (
            self.pd_data["Is Forward"].fillna(False).astype(bool)
        )
        self.pd_data = self.pd_data[~self.pd_data["Is Forward"]]
        return self

    def write_data(self, path="data/excel/clean_data.xlsx"):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.pd_data.to_excel(path, index=False)
