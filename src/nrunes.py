import json
import pandas as pd
from typing import List, Dict
import csv
from constants import *
import os

# This script perfroms n-gram analyses on runestrings.
# Analysis structure: Every runic sequence is treated as a document, every individual rune is treated as a token.
# N-Gram analysis thus delivers data on the combination of individual runes and their variations

# Basic Functions
# ---------------


def load_data(input_file = NRUNES_INFILE) -> List[Dict[str, str | int]]:
    try:
        with open(input_file, 'r', encoding="UTF-8") as f:
            raw_rune_string = json.load(f)
    except:
        print("Error loading data. Make sure you provided input data.")
    return raw_rune_string


def doc_builder(data: List[Dict[str, str | int]]) -> List[List[str]]:
    docs_list = [x['runestring'] for x in data]
    tokenized_docs = [x.split(',') for x in docs_list]
    return tokenized_docs


def nested_runestring_ngrammer(data: List[List[str]], stepsize: int = 1) -> List[List[str]]:
    all_grams: List[List[str]] = []
    for runestring in data:
        shit = simple_ngrammer(runestring, stepsize)
        all_grams.append(shit)
    return all_grams


def simple_ngrammer(data: List[str], stepsize: int):
    temp = zip(*[data[i:] for i in range(stepsize)])
    n_grams = ["_".join(ngram) for ngram in temp]
    return n_grams


def gram_sorter(data: List[List[str]]) -> pd.DataFrame:
    flat_grams = [x for y in data for x in y]
    df = pd.DataFrame(flat_grams)
    df = df.groupby(df.columns.tolist(),as_index=False).size()
    df = df.sort_values(by='size', ascending=False)
    df = df.reset_index(drop=True)
    return df


# API Methods
# -----------

def get_standard_data(input_data = NRUNES_INFILE, stepsize=4, cache: bool = True, usecache: bool = True) -> Dict[int, pd.DataFrame]:
    if usecache and len(os.listdir('displayData')) == 4:
        gram_dfs: Dict[int, pd.DataFrame]
        for i in os.listdir('displayData'):
            df = pd.read_json(f'displayData/{i}')
            dfno = int(i[0])
            gram_dfs[dfno] = df
        return gram_dfs
    else: 
        d1 = load_data(input_data)
        d2 = doc_builder(d1)
        gram_dfs: Dict[int, pd.DataFrame] = {}
        for i in range(2, stepsize+1):
            n_grams = nested_runestring_ngrammer(d2, i)
            df = gram_sorter(n_grams)
            if cache:
                df.to_json(f"{FRONTEND_DELIVERY_DIR}{i}-{FRONTEND_FILE_SUFFIX}")
            gram_dfs[i] = df
        return gram_dfs


# CLI Methods
# -----------

# Use these methods when working from the command line.

def analyze(input_data = NRUNES_INFILE, stepsize=2, output_filename: str = NGRAM_RESULT_JSON) -> None:
    """This function should handly everything neccessary when working from the command line.
        Params:
            input_data (str): Path to a json file containing the runestrings to be analyzed.
            stepsize (int): what kind of n-grams you want. 2=Bigrams, 3=Trigrams etc."""
    d1 = load_data(input_data)
    d2 = doc_builder(d1)
    n_grams = nested_runestring_ngrammer(d2, stepsize)
    df = gram_sorter(n_grams)
    df.to_json(output_filename)
    print('Here are the results:')
    print(df)
    print('The results have been exported as json.')
    print('Done')



if __name__ == "__main__":
    d1 = load_data()
    d2 = doc_builder(d1)
    n_grams = nested_runestring_ngrammer(d2, stepsize=2)
    gram_sorter(n_grams)
    