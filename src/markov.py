import spacy
import re
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
import os
from  itertools import chain
warnings.filterwarnings('ignore')

nlp = spacy.load('en_core_web_sm')
data_path = './data/text/text/'
output_file_path = './data/text/hagrid-hole-data-markov.txt'

def read_file_data (file):
    with open (file, 'r')  as f:
        raw_file_text = f.read()
    return raw_file_text

def generate_model_from_data_files (files):
    models = []
    for file in files:
        file_text = read_file_data(data_path + file)
        hagrid_text = "".join(chain.from_iterable(file_text))
        if len(hagrid_text) < 100000:
            model = markovify.Text(hagrid_text)
            models.append(model)
    final_model = markovify.combine(models)
    return final_model

files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
model = generate_model_from_data_files(files)
model_json = model.to_json()
with open('./saved_markov_model/markov_model.json', 'w') as wf:
    wf.write(model_json)

for i in range(50):
    sentence = model.make_sentence()
    short = model.make_short_sentence(max_chars=100)
    with open('out.txt', 'a+') as wf:
        wf.write(f'>> {sentence}\n')
        wf.write(f'>> {short}\n')