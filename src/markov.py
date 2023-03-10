from pathlib import Path
import spacy
import re
import markovify
import nltk
import warnings
warnings.filterwarnings('ignore')

def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
    text = ' '.join(text.split())
    return text

data_str = ''
files = [str(x) for x in Path("./data/text/text/").glob("**/*.txt")]
x = 0
for file in files:
    with open(file, 'r') as file:
        data = file.read()
    text = text_cleaner(data)
    data_str += text + '\n'
    if x == 20:
        break
    x = x + 1

print(data_str[:100])

nlp = spacy.load('en_core_web_sm')
text_doc = nlp(data_str)
text_sents = ' '.join([sent.text for sent in text_doc.sents if len(sent.text) > 1])

gen_1 = markovify.Text(text_sents, state_size=3)
for i in range(5):
    print(gen_1.make_sentence())