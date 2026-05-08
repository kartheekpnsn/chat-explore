# Load System Modules
import logging
import os
import pickle
import sys

import pandas as pd
import tqdm

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    from src.integrations.llm import OpenAIUtils
    pd_data = pd.read_excel("data/excel/clean_data.xlsx")
    openai_utils = OpenAIUtils()
    if not openai_utils._available:
        print("LLM not available. Translation skipped.")
        sys.exit(0)
    if os.path.exists("data/pickle/translated_txt.pkl"):
        with open("data/pickle/translated_txt.pkl", "rb") as f:
            translated_txt_dict = pickle.load(f)
    else:
        translated_txt_dict = {}
    for msg in tqdm.tqdm(pd_data["Message"].tolist()):
        if msg in translated_txt_dict:
            continue
        translated_txt = openai_utils.call_llm(msg)
        if translated_txt is None:
            translated_txt = msg
        translated_txt_dict[msg] = translated_txt
        with open("data/pickle/translated_txt.pkl", "wb") as f:
            pickle.dump(translated_txt_dict, f)
