import os
import json

# Get the directory to store JSON files from the user
output_dir = input("Enter the directory to store JSON files: ")

# Get the input file with sentences from the user
input_file = input("Enter the path to the input file with sentences: ")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r') as file:
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
