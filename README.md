# Runic n-grams

This is a relatively simple script and web app to generate n-grams within strings of futhark characters. It collates n-grams, or rather n-graphs,
yielding a results table indicating how often specific runes occur together.
This script was specifically written for the work of Dr. Elisabeth Magin. It works only with Dr. Magins system for variation sensitive encoding of 
futhark characters.

## Runing the app

There are two ways of running this application. You can either refer to the instance of the web app hosted in the Streamlit Community Cloud at the link here:

ADD LINK!

or you can run this web app locally using pipenv.
To do this, clone this repository and install dependencies using `pipenv install`.
You can start the webapp from the command line using `pipenv run webapp` and run the analysis
script using `pipenv run n-runer`.
Please note that the script will look for a file named "nrunes.json" in the "data/input/" folder
and save the results as json files in the "data/results" folder.