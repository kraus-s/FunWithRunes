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


def load_data(inputFile = NRUNES_INFILE) -> List[Dict[str, str or int]]:
    try:
        with open(inputFile, 'r', encoding="UTF-8") as f:
            rawRunes = json.load(f)
    except:
        print("Error loading data. Make sure you provided input data.")
    return rawRunes


def doc_builder(data: List[Dict[str, str or int]]) -> List[List[str]]:
    docsList = [x['runestring'] for x in data]
    tokenizedDocs = [x.split(',') for x in docsList]
    return tokenizedDocs


def nested_runestring_ngrammer(data: List[List[str]], stepsize: int = 1) -> List[List[str]]:
    allGrams: List[List[str]] = []
    for runestring in data:
        shit = simple_ngrammer(runestring, stepsize)
        allGrams.append(shit)
    return allGrams


def simple_ngrammer(data: List[str], stepsize: int):
    temp = zip(*[data[i:] for i in range(stepsize)])
    n_grams = ["_".join(ngram) for ngram in temp]
    return n_grams


def _gramSorter(data: List[List[str]]) -> pd.DataFrame:
    flatGrams = [x for y in data for x in y]
    df = pd.DataFrame(flatGrams)
    df = df.groupby(df.columns.tolist(),as_index=False).size()
    df = df.sort_values(by='size', ascending=False)
    df = df.reset_index(drop=True)
    return df


# API Methods
# -----------

def get_standard_data(inputData = NRUNES_INFILE, stepsize=4, cache: bool = True, usecache: bool = True) -> Dict[int, pd.DataFrame]:
    if usecache and len(os.listdir('displayData')) == 4:
        gramDfs: Dict[int, pd.DataFrame]
        for i in os.listdir('displayData'):
            df = pd.read_json(f'displayData/{i}')
            dfno = int(i[0])
            gramDfs[dfno] = df
        return gramDfs
    else: 
        d1 = load_data(inputData)
        d2 = doc_builder(d1)
        gramDfs: Dict[int, pd.DataFrame] = {}
        for i in range(2, stepsize+1):
            nGrams = nested_runestring_ngrammer(d2, i)
            df = _gramSorter(nGrams)
            if cache:
                df.to_json(f"displayData/{i}-gram-result.json")
            gramDfs[i] = df
        return gramDfs


# CLI Methods
# -----------

# Use these methods when working from the command line.

def analyze(inputData = NRUNES_INFILE, stepsize=2, output_filename: str = NGRAM_RESULT_JSON) -> None:
    """This function should handly everything neccessary when working from the command line.
        Params:
            inputData (str): Path to a json file containing the runestrings to be analyzed.
            stepsize (int): what kind of n-grams you want. 2=Bigrams, 3=Trigrams etc."""
    d1 = load_data(inputData)
    d2 = doc_builder(d1)
    nGrams = nested_runestring_ngrammer(d2, stepsize)
    df = _gramSorter(nGrams)
    df.to_json(NGRAM_RESULT_JSON)
    print('Here are the results:')
    print(df)
    print('The results have been exported as json.')
    print('Done')



if __name__ == "__main__":
    d1 = load_data()
    d2 = doc_builder(d1)
    nGrams = nested_runestring_ngrammer(d2, stepsize=2)
    _gramSorter(nGrams)
    