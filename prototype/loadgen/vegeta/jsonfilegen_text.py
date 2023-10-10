import os
import json

# Directory to store JSON files
# output_dir = 'prompt_jsons'
output_dir = 'mask_jsons'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read sentences from the text file
# sentences_file = '../data/prompts/sentences.txt'
sentences_file = '../data/context/masked_sentences.txt'

with open(sentences_file, 'r') as file:
    sentences = file.readlines()

# Process each sentence and save it as a JSON file
for i, sentence in enumerate(sentences):
    # Remove leading and trailing whitespace
    sentence = sentence.strip()

    # Create a dictionary with a "data" field containing the sentence
    data = {'data': sentence}

    # Generate a unique filename for each JSON file (e.g., data_1.json, data_2.json, ...)
    json_filename = os.path.join(output_dir, f'data_{i + 1}.json')

    # Write the dictionary to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file)

    print(f'Saved: {json_filename}')
