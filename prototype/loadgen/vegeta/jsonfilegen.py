import os
import base64
import json

# Directory containing the images
image_directory = '../data/images'

# Output directory for JSON files
output_directory = '/home/srishankar/loadtestdata'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through each image in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(('.JPEG')):
        # Read the image data
        with open(os.path.join(image_directory, filename), 'rb') as image_file:
            image_data = image_file.read()

        # Encode the image data to base64
        base64_data = base64.b64encode(image_data).decode('utf-8')

        # Create a dictionary with the "data" field
        data_dict = {"data": base64_data}

        # Create a JSON file for each image
        json_filename = os.path.splitext(filename)[0] + '.json'
        json_filepath = os.path.join(output_directory, json_filename)

        # Write the JSON data to the file
        with open(json_filepath, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)

        print(f"Created JSON file: {json_filepath}")
