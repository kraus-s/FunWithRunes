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


if __name__ == '__main__':
    welcome()
    gramDFs = nrunes.get_standard_data()
    selectGram = st.selectbox(label='Select ngram level you want to display (2=bigram, 3=trigram etc.):', options=gramDFs.keys(), index=0)
    st.table(gramDFs[selectGram])
    st.header('About')
    st.write('All data and code are available on GitHub at: https://albertauyeung.github.io/2018/06/03/generating-ngrams.html/')