#!/bin/bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader words
python -m nltk.downloader stopwords
