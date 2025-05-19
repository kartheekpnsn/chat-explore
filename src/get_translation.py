# Load System Modules --------------------------------------------------------------------------------------------------
import os
import pickle
import sys

import pandas as pd
import tqdm

sys.path.append(os.path.abspath(os.path.join("src/")))

from llm import OpenAIUtils

if __name__ == "__main__":
    pd_data = pd.read_excel("data/excel/clean_data.xlsx")
    openai_utils = OpenAIUtils()
    if os.path.exists("data/pickle/translated_txt.pkl"):
        with open("data/pickle/translated_txt.pkl", "rb") as f:
            translated_txt_dict = pickle.load(f)
    else:
        translated_txt_dict = {}
    for msg in tqdm.tqdm(pd_data["Message"].tolist()):
        if msg in translated_txt_dict:
            continue
        try:
            translated_txt = openai_utils.call_llm(msg)
        except Exception as e:
            print(f"Unable to translate. Reason: {e}, while translating message: {msg}")
            translated_txt = msg
        translated_txt_dict[msg] = translated_txt
        with open("data/pickle/translated_txt.pkl", "wb") as f:
            pickle.dump(translated_txt_dict, f)
