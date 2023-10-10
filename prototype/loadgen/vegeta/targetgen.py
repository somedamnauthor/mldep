import os

# Directory containing the JSON files
# json_directory = 'image_jsons'
json_directory = 'mask_jsons'

# Output file for post_targets.txt
output_file = 'ptargs_masks.txt'

# Initialize an empty list to store the target URLs
target_urls = []

# Loop through each JSON file in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        # Construct the target URL for each JSON file
        target_url = f"POST http://localhost:6000/predict\nContent-Type: application/json\n@{json_directory}/{filename}"
        target_urls.append(target_url)

# Write the target URLs to the output file
with open(output_file, 'w') as file:
    file.write('\n\n'.join(target_urls))

print(f"Created {output_file} with {len(target_urls)} target URLs.")
