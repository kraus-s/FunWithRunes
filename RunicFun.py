import streamlit as st
import pandas as pd
from constants import *
from pathlib import Path
import nrunes


def welcome():
    st.title('Welcome to fun with runes!')
    st.write('''This webapp is a companion to the research done by Dr. Elisabeth Magin. All data is taken from her research and provided by her.
                All code is written by Sven Kraus at the University of Basel.''')
    st.write('''For now all you can display are the results of an n-gram analysis of the entire corpus of Elisabeths PhD research. For the purpose of this analysis, 
                every runic sequence was considered a document and tokenized on a grapheme level, i.e. every rune is its own token. The n-grams shown and counts
                provided show the frequency with which every n-gram of individual runes occurs in the corpus.''')

def get_data():
    inFile = Path(NGRAM_RESULT_JSON)
    if inFile.is_file():
        df = pd.read_json(NGRAM_RESULT_JSON)
    else:
        df = nrunes.get_standard_data()
    return df


if __name__ == '__main__':
    welcome()
    df = get_data()
    st.write('Below you can see the static results of a bigram analysis')
    st.table(df)
    st.header('About')
    st.write('All data and code are available on GitHub at: https://albertauyeung.github.io/2018/06/03/generating-ngrams.html/')