import os
import base64
import json

# Get the directory containing the images from the user
input_directory = input("Enter the path to the directory containing the images: ")

# Get the output directory for JSON files from the user
output_directory = input("Enter the path to the output directory for JSON files: ")

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through each image in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.JPEG')):
        # Read the image data
        with open(os.path.join(input_directory, filename), 'rb') as image_file:
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

