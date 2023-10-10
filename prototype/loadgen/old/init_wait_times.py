import csv
import numpy as np

scale = 0.01

sample_list = []

with open('tweet_load.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        
        try:
            num = round(int(row['tweets']) * scale)
            lam = (60 * 1000.0) / num
            samples = np.random.poisson(lam, num)
        
        except:
            print("Error in row:",row)
            samples = []
        
        sample_list.append(samples)

print('done')


with open('wait_times.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for sublist in sample_list:
        writer.writerow(sublist)