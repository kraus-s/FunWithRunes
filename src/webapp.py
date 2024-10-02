import streamlit as st
import pandas as pd
from constants import *
import nrunes


def welcome():
    st.title('Welcome to the n-runes web app!')
    st.write('''This webapp is a companion to the research done by Dr. Elisabeth Magin. All data is taken from her research and provided by her.
                All code is written by Sven Kraus at the University of Basel / Humboldt-Universität zu Berlin.
                You can find the code on GitHub: https://github.com/kraus-s/n-runes''')
    st.write('''For now all you can display are the results of an n-gram analysis of the entire corpus of Elisabeth's PhD research. For the purpose of this analysis, 
                every runic sequence was considered a document and tokenized on a grapheme level, i.e. every rune is its own token. The n-grams shown and counts
                provided show the frequency with which every n-gram of individual runes occurs in the corpus.''')


if __name__ == '__main__':
    welcome()
    gram_dfs = nrunes.get_standard_data()
    variance = st.selectbox(label="Do you want you want to display n-grams for runes with numeric variance encoding or without?", options=gram_dfs.keys(), index=0)
    select_gram = st.selectbox(label='Select ngram level you want to display (2=bigram, 3=trigram etc.):', options=gram_dfs[variance].keys(), index=0)
    st.dataframe(gram_dfs[variance][select_gram], hide_index=True, use_container_width=True)