import os
import json

# Get every file in the raw data folder and store the filename in an array
data_path = "./data/raw/"
files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

# Go through every file and normalize the raw data into the correct format
# This step has to be performed because of the chunk of data gathered early on
# in the bot's life didn't have the message author  attached to the message.
# We need to normalize the data to ascribe to the correct API and have message author
# be "unknown" for these messages
for filename in files:
    break