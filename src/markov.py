import spacy
import markovify
import warnings
import os
from datetime import datetime
from itertools import chain
warnings.filterwarnings('ignore')

nlp = spacy.load('en_core_web_sm')
data_path = './data/text/text/'

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

def generate_text_output_from_model (model):
    sentences = []
    for _ in range(50):
        longSentence = f'>> {model.make_sentence()}\n'
        shortSentence = f'>> {model.make_short_sentence(max_chars=100)}\n'
        sentences.append(longSentence)
        sentences.append(shortSentence)
    with open(f'./out/out-{datetime.now()}.txt', 'a+') as wf:
        for s in sentences:
            wf.write(s)

files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
model = generate_model_from_data_files(files)
model_json = model.to_json()    # model can be reloaded with markovify.Text.from_json(model_json)
with open('./saved_markov_model/markov_model.json', 'w') as wf:
    wf.write(model_json)
generate_text_output_from_model(model)