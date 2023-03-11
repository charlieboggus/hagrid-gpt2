import os
import re
import json

# Modify this method to determine how the text we use to train our model is formatted
def text_cleaner(text):
    text = text + ". "
    text = re.sub(r'.*\bhttps?:\/\/\S+.*', '', text)
    text = re.sub(r'[^a-zA-Z.,\s]', '', text)
    # text = re.sub(r'<.*:[a-zA-Z0-9_]+:\d+>', '', text)
    # text = re.sub(r'<@\d+>', '', text)
    # text = "<s>" + text + "</s>"
    text = ' '.join(text.split())
    return text

# Iterate through every input file, clean the text data contained within, and write it to output files
input_data_path = "./data/text/raw/"
files = [f for f in os.listdir(input_data_path) if os.path.isfile(os.path.join(input_data_path, f))]
for filename in files:
    rf = open(f'./data/text/raw/{filename}')
    json_data = json.load(rf) # this is either a string[] or a { message, author }[]
    rf.close()
    with open(f'./data/text/json/{filename}.json', "w") as wf:
        wf.write(json.dumps(json_data))
    
    messages = []
    if isinstance(json_data[0], str):
        # data is just a string array ["message1", "message2"]
        for obj in json_data:
            message = text_cleaner(obj)
            messages.append(message)
        with open(f'./data/text/text/{filename}.txt', "w") as wf:
            wf.write("\n".join(messages))
    else:
        # data looks like: [{ 'message': 'x', 'author': 'y' }, ... ]
        for obj in json_data:
            message = text_cleaner(obj['message'])
            messages.append(message)
    with open(f'./data/text/text/{filename}.txt', "w") as wf:
        wf.write("\n".join(messages)) 