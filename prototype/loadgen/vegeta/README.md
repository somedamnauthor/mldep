# Usage Steps

1. Place your data inside the ../data folder

2. Use jsonfilegen_images.py or jsonfilegen_text.py in order to generate a set of JSONs from the dataset. Alternatively use these files as a template to write your own data->json converter. This step creates a JSON file for every individual datapoint

3. Use targetgen.py to create a single targets file that is to be read by vegeta. Provide targetgen.py the directory where the JSON files created in the previous step are stored

4. Create a (prefereably empty) folder titled 'logs'

4. Use gen_commands.py to generate commands according to the load. Commands will be saved onto a file called vegeta_commands.sh, which can then be run. The commands will store logs into the logs folder
