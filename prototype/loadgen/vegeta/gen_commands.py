import csv

# Get the scale factor from the user
scale_factor = float(input('Enter the scale factor for tweets (default is 1.0): ') or 1.0)

# Get the target file path from the user
target_file = input('Enter the path to the target file: ')

load_file = input('Enter the path to the trace file used for the load (Eg: ../loadsample_2.csv): ')

# Load the CSV file
with open(load_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Initialize a counter for the output file names
    file_counter = 1

    # Open a file to store the generated commands
    with open('vegeta_commands.sh', 'w') as output_file:
        for row in csv_reader:
            # Extract the 'tweets' value from the CSV row and apply the scale factor
            tweets = int(float(row['tweets']) * scale_factor)

            # Generate the output file name using the counter
            output_file_name = 'results_{}.json'.format(file_counter)

            # Increment the counter for the next file
            file_counter += 1

            # Generate the Vegeta attack command with the unique output file name
            vegeta_command = f'./vegeta attack -header "Content-Type: application/json" -rate={tweets}/1m -duration=1m -targets={target_file} | ./vegeta encode > logs/{output_file_name}\n'

            # Write the generated command to the output file
            output_file.write(vegeta_command)
