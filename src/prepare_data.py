import os
import json

# Get every file in the raw data folder and store the filename in an array
data_path = "./data/text/raw/"
files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

for filename in files:
    rf = open(f'./data/text/raw/{filename}')
    json_data = json.load(rf) # this is either a string[] or a { message, author }[]
    rf.close()
    with open(f'./data/text/json/{filename}.json', "w") as wf:
        wf.write(json.dumps(json_data))
    
    if isinstance(json_data[0], str):
        messages = "\n".join(json_data)
        with open(f'./data/text/text/{filename}.txt', "w") as wf:
            wf.write(messages)
    else:
        # data looks like: [{ 'message': 'x', 'author': 'y' }, ... ]
        messages = []
        for obj in json_data:
            message = obj['message']
            messages.append(message)
        with open(f'./data/text/text/{filename}.txt', "w") as wf:
            wf.write("\n".join(messages))