import csv
import argparse

# Create an argument parser to handle runtime arguments
parser = argparse.ArgumentParser(description='Generate Vegeta attack commands')
parser.add_argument('--scale-factor', type=float, default=1.0, help='Scale factor for tweets')
parser.add_argument('--target-type', choices=['prompts', 'masks', 'images'], default='images', help='Target type')
args = parser.parse_args()

# Load the CSV file
with open('../loadsample_2.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Initialize a counter for the output file names
    file_counter = 1

    # Open a file to store the generated commands
    with open('vegeta_commands.sh', 'w') as output_file:
        for row in csv_reader:
            # Extract the 'tweets' value from the CSV row and apply the scale factor
            tweets = int(float(row['tweets']) * args.scale_factor)

            # Determine the target file based on the target type
            if args.target_type == 'prompts':
                target_file = 'ptargs_prompts.txt'
            elif args.target_type == 'masks':
                target_file = 'ptargs_masks.txt'
            else:
                target_file = 'ptargs_images.txt'

            # Generate the output file name using the counter
            output_file_name = f'results_{file_counter}.json'

            # Increment the counter for the next file
            file_counter += 1

            # Generate the Vegeta attack command with the unique output file name
            vegeta_command = f'./vegeta attack -header "Content-Type: application/json" -rate={tweets}/1m -duration=1m -targets={target_file} | ./vegeta encode > logs/{output_file_name}\n'

            # Write the generated command to the output file
            output_file.write(vegeta_command)
