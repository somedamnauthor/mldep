import os

# Get the directory containing the JSON files from the user
json_directory = input("Enter the directory containing the JSON files: ")

# Get the output file name from the user
output_file = input("Enter the name of the output file (e.g., ptargs_prompts.txt): ")

# Get the deployment endpoint from the user
deployment_endpoint = input("Enter the deployment endpoint (e.g., http://localhost:6000/predict): ")

# Initialize an empty list to store the target URLs
target_urls = []

# Loop through each JSON file in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        # Construct the target URL for each JSON file
        target_url = f"POST {deployment_endpoint}\nContent-Type: application/json\n@{os.path.join(json_directory, filename)}"
        target_urls.append(target_url)

# Write the target URLs to the output file
with open(output_file, 'w') as file:
    file.write('\n\n'.join(target_urls))

print(f"Created {output_file} with {len(target_urls)} target URLs.")
