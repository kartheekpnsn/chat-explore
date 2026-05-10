import json
import os

import pandas as pd


class MetricsStore:

    def __init__(self, path="data/json/"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def _filepath(self, key):
        return os.path.join(self.path, f"{key}.json")

    def save_df(self, key, df):
        df.to_json(self._filepath(key), orient="records", indent=2, default_handler=str)

    def load_df(self, key):
        return pd.read_json(self._filepath(key), orient="records")

    def save_json(self, key, data):
        with open(self._filepath(key), "w") as f:
            json.dump(data, f, indent=2)

    def load_json(self, key):
        with open(self._filepath(key)) as f:
            return json.load(f)
