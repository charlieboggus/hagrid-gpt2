import os
import tensorflow as tf
from transformers import GPT2Config, TFGPT2LMHeadModel, GPT2Tokenizer, WEIGHTS_NAME, CONFIG_NAME

save_path = './data/tokenized_data/'
tokenizer = GPT2Tokenizer.from_pretrained(save_path)
tokenizer.add_special_tokens({
    "bos_token": "<s>",
    "eos_token": "</s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})
config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    eos_token_id=tokenizer.eos_token_id,
    bos_token_id=tokenizer.bos_token_id
)
model = TFGPT2LMHeadModel(config)

data_str = ''
data_path = "./data/text/text/"
files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
for filename in files:
    with open(data_path + filename, 'r', encoding='utf-8') as rf:
        x = rf.read()
    data_str += x
data_str_tokenized = tokenizer.encode(data_str)

examples = []
block_size = 100
batch_size = 32
buffer_size = 1000

for i in range(0, len(data_str_tokenized) - block_size + 1, block_size):
    examples.append(data_str_tokenized[i:i + block_size])

inputs = []
labels = []

for ex in examples:
    inputs.append(ex[:-1])
    labels.append(ex[1:])

dataset = tf.data.Dataset.from_tensor_slices((inputs, labels))
dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

optimizer = tf.keras.optimizers.Adam(learning_rate=6.25e-5, epsilon=1e-08, clipnorm=1.0)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric  = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

model.compile(optimizer=optimizer, loss=[loss, *[None] * model.config.n_layer], metrics=[metric])
num_epoch = 3
history = model.fit(dataset, epochs=num_epoch)

# Save the model
output_dir = './saved_gpt2_model/'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

save_model = model.module if hasattr(model, 'module') else model
output_model_file = os.path.join(output_dir, WEIGHTS_NAME)
output_config_file = os.path.join(output_dir, CONFIG_NAME)

model.save_pretrained(output_dir)
save_model.config.to_json_file(output_config_file)
tokenizer.save_pretrained(output_dir)