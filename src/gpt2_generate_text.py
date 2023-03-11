import os
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

gpt2_model_dir = './saved_gpt2_model/'

# Load the saved model
tokenizer = GPT2Tokenizer.from_pretrained(gpt2_model_dir)
model = TFGPT2LMHeadModel.from_pretrained(gpt2_model_dir)

user_input_ids = tokenizer.encode(
    tokenizer.eos_token + input(">> User: "), 
    return_tensors='tf'
)
bot_output = model.generate(
    user_input_ids, 
    max_length=100, 
    num_beams = 5,
    temperature = 0.7,
    no_repeat_ngram_size=2,
    num_return_sequences=5
)
for x in bot_output:
    print(f">> Bot: {tokenizer.decode(x, skip_special_tokens=True)}")