import os
import re
import json

# Modify this method to determine how the text we use to train our model is formatted
def clean_emotes (text):
    result = ''
    words = text.split(' ')
    for word in words:
        tmp = word
        if re.search(r'<:[a-zA-Z0-9]+:\d+>', tmp):
            tmp = tmp[2:]
            string = ''
            for c in tmp:
                if not c == ':':
                    string = string + c
                else:
                    break
            tmp = string
        if len(tmp) == 0:
            result = result + ''
        elif word[-1] == '.':
            result = result + tmp + '. '
        else:
            result = result + tmp + ' '
    return result

def clean_users (text):
    rf = open('./data/users.json')
    users = json.load(rf)
    rf.close()
    result = ''
    words = text.split(' ')
    for word in words:
        tmp = word
        if re.search(r'<@(\d+)>', word):
            tmp = re.sub(r'\D', '', tmp)
        if tmp in users:
            tmp = users[tmp]
        
        if len(tmp) == 0:
            result = result + ''
        elif tmp[-1] == '.':
            result = result + tmp + '. '
        else:
            result = result + tmp + ' '
    return result

def clean_non_sentence_lines (text):
    if text == '.' or text == ' ' or text == '. ' or text == ' ':
        return ''
    else:
        return text

def text_cleaner(text):
    result = text
    result = re.sub(r'.*\bhttps?:\/\/\S+.*', '', result)            # remove urls
    result = clean_emotes(result)                                   # clean emotes
    result = clean_users(result)                                    # clean user @'s
    result = re.sub(r'[^a-zA-Z0-9.,\s]', '', result)                # Remove whacky characters
    result = clean_non_sentence_lines(result)                       # if a line is just . or blank after cleaning, get rid of it
    result = result + ". "                                          # end each sentence with a period so the model knows where a sentence ends
    result = re.sub(r'\s+\.', '.', result)                          # remove space before period at end of sentence (not sure why thats added..)
    # text = "<s>" + text + "</s>"                                  # this is just for GPT-2 training data
    result = ' '.join(result.split())
    return result

# Iterate through every input file, clean the text data contained within, and write it to output files
input_data_path = "./data/text/raw/"
files = [f for f in os.listdir(input_data_path) if os.path.isfile(os.path.join(input_data_path, f))]
for filename in files:
    rf = open(f'{input_data_path}{filename}')
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
    else:
        # data looks like: [{ 'message': 'x', 'author': 'y' }, ... ]
        for obj in json_data:
            message = text_cleaner(obj['message'])
            messages.append(message)
    with open(f'./data/text/text/{filename}.txt', "w") as wf:
        wf.write("\n".join(messages)) 