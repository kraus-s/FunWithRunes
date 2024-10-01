import json
import pandas as pd
from constants import *
import os
import glob

# This script perfroms n-gram analyses on runestrings.
# Analysis structure: Every runic sequence is treated as a document, every individual rune is treated as a token.
# N-Gram analysis thus delivers data on the combination of individual runes and their variations

# Basic Functions
# ---------------


def load_data(input_file = NRUNES_INFILE) -> list[dict[str, str | int]]:
    try:
        with open(input_file, 'r', encoding="UTF-8") as f:
            raw_rune_string = json.load(f)
    except:
        print("Error loading data. Make sure you provided input data.")
    return raw_rune_string


def doc_builder(data: list[dict[str, str | int]], varied: bool = True) -> list[list[str]]:
    """This function tokenizes the input runestrings. It can to so in two ways:
    If varied is set to True, it will consider variants of normalized runes as separate tokens.
    If varied is set to False, it will not consider the variants as established in Elisabeth Magins encoding."""
    docs_list = [x['runestring'] for x in data]
    if varied:
        tokenized_docs = [x.split(',') for x in docs_list]
    elif not varied:
        tokenized_docs_varied = [x.split(',') for x in docs_list]
        tokenized_docs = []
        for i in tokenized_docs_varied:
            current_doc = []
            for ii in i:
                iii = "".join([x for x in ii if not x.isdigit()])
                current_doc.append(iii)
            tokenized_docs.append(current_doc)
    return tokenized_docs


def nested_runestring_ngrammer(data: list[list[str]], stepsize: int = 1) -> list[list[str]]:
    all_grams: list[list[str]] = []
    for runestring in data:
        shit = simple_ngrammer(runestring, stepsize)
        all_grams.append(shit)
    return all_grams


def simple_ngrammer(data: list[str], stepsize: int):
    temp = zip(*[data[i:] for i in range(stepsize)])
    n_grams = ["_".join(ngram) for ngram in temp]
    return n_grams


def gram_sorter(data: list[list[str]]) -> pd.DataFrame:
    flat_grams = [x for y in data for x in y]
    df = pd.DataFrame(flat_grams)
    df = df.groupby(df.columns.tolist(),as_index=False).size()
    df = df.sort_values(by='size', ascending=False)
    df = df.reset_index(drop=True)
    return df




# Methods
# -----------

def get_standard_data(data_dir: str = FRONTEND_DELIVERY_DIR) -> dict[int, pd.DataFrame]:
    gram_dfs: dict[int, pd.DataFrame] = {"varied": {}, "unvaried": {}}
    for i in glob.glob(f"{FRONTEND_DELIVERY_DIR}*.json"):
        with open(i, "r", encoding="utf-8") as f:
            df = pd.read_json(f)
        name = i.split("/")[-1]
        name_parts = name.split("-")
        df.rename(columns={"0": "rune-gram", "size": "frequency"}, inplace=True)
        gram_dfs[name_parts[0]][int(name_parts[1])] = df
    return gram_dfs


def analyze(input_data: str = NRUNES_INFILE, stepsize: int = 4, verbose: bool = False, varied: bool = True):    
    """This function will produce 2, 3, and 4-grams data and drop the results in the data/results directory.
     Input file should be namend nrunes.json and should be in the data directory, unless otherwise specified."""
    # TODO: Refactor, this could be done more neatly

    d1 = load_data(input_data)
    d2 = doc_builder(d1, varied)

    gram_dfs: dict[int, pd.DataFrame] = {}
    for i in range(2, stepsize+1):
        n_grams = nested_runestring_ngrammer(d2, i)
        df = gram_sorter(n_grams)
        if varied:
            df.to_json(f"{FRONTEND_DELIVERY_DIR}varied-{i}{FRONTEND_FILE_SUFFIX}")
        elif not varied:
            df.to_json(f"{FRONTEND_DELIVERY_DIR}unvaried-{i}{FRONTEND_FILE_SUFFIX}")
        if verbose:
            print(f'{i}-grams have been exported as json.')
            print(df)
        gram_dfs[i] = df
    print('Done')


def main():
    """This function will run the analysis on the nrunes.json file in the data directory.
    By default, it will analyze the data with varied=True and varied=False."""
    analyze(varied=True)
    analyze(varied=False)

if __name__ == "__main__":
    main()
    