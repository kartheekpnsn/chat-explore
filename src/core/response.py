from typing import Optional

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.utils.action_logging import Logger


class Response:
    def __init__(self, data: Optional[pd.DataFrame] = None, logger=None):
        if logger is None:
            self.logger = Logger(
                log_flag=True, log_file="response", log_path="../logs/"
            )
        else:
            self.logger = logger
        self.data = data

    def compute(self) -> dict:
        """
        Returns per-user response stats.
        A response event is a turn switch: the first message from user B after
        user A's last consecutive message. Response time = gap between those two
        timestamps.
        Returns dict keyed by user name:
            {"median_response_min": float|None, "p75_response_min": float|None,
             "n_responses": int}
        """
        if self.data is None or self.data.empty:
            return {}

        df = self.data.sort_values("Timestamp").reset_index(drop=True)
        users = df["User"].unique().tolist()
        result = {
            u: {"median_response_min": None, "p75_response_min": None, "n_responses": 0}
            for u in users
        }

        response_times: dict[str, list[float]] = {u: [] for u in users}

        prev_user = df.iloc[0]["User"]
        prev_ts = df.iloc[0]["Timestamp"]

        for _, row in df.iloc[1:].iterrows():
            curr_user = row["User"]
            curr_ts = row["Timestamp"]
            if curr_user != prev_user:
                gap = (curr_ts - prev_ts).total_seconds() / 60.0
                response_times[curr_user].append(gap)
            prev_user = curr_user
            prev_ts = curr_ts

        for user, times in response_times.items():
            if times:
                s = pd.Series(times)
                result[user]["n_responses"] = len(times)
                result[user]["median_response_min"] = round(float(s.median()), 3)
                result[user]["p75_response_min"] = round(float(s.quantile(0.75)), 3)

        return result

    def get_the_longest_conversation_date(self) -> Optional[str]:
        """
        Returns the date with the most active back-and-forth conversation,
        scored by Bayesian-adjusted response frequency.
        """
        if self.data is None or self.data.empty:
            return None

        df = self.data.sort_values("Timestamp").reset_index(drop=True)
        df = df.copy()
        df["Date"] = df["Timestamp"].dt.strftime("%d-%b-%Y")

        grouped = (
            df.groupby(["User", "Timestamp"])["Message"]
            .count()
            .reset_index()
            .sort_values("Timestamp")
        )
        grouped["Date"] = grouped["Timestamp"].dt.strftime("%d-%b-%Y")
        grouped["Response (Min)"] = (
            grouped["Timestamp"].diff().dt.total_seconds().div(60).fillna(0)
        )

        grp1 = grouped.groupby("Date")["Response (Min)"].mean().reset_index()
        grp2 = grouped.groupby("Date")["Message"].count().reset_index()
        merged = grp1.merge(grp2, on="Date", how="left")

        if merged.empty:
            return None

        scaler = MinMaxScaler()
        v = 1 - scaler.fit_transform(merged[["Response (Min)"]])[:, 0]
        r = merged["Message"].values
        vxr = v * r
        merged["Final Score"] = (vxr + vxr.sum()) / (v + v.sum())
        merged = merged.sort_values("Final Score", ascending=False)
        return merged.iloc[0]["Date"]
