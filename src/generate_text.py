import os
from transformers import BertTokenizer, TFAutoModel

fs = [f for f in os.listdir('./saved_model/') if os.path.isfile(os.path.join('./saved_model/', f))]
print(fs)

tokenizer = BertTokenizer.from_pretrained('./saved_model/')
model = TFAutoModel.from_pretrained('./saved_model/')

#tokenizer = GPT2Tokenizer.from_pretrained("saved_model/", local_files_only=True)
#model = TFGPT2LMHeadModel.from_pretrained("saved_model/", local_files_only=True)

input_text = input()
input_ids = tokenizer.encode(input_text, return_tensors='tf')
beam_output = model.generate(
    input_ids,
    max_length=100,
    num_beams = 5,
    temperature = 0.7,
    no_repeat_ngram_size=2,
    num_return_sequences=5
)
print(tokenizer.decode(beam_output[0]))