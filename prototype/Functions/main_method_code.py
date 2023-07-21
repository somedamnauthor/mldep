

# Instantiate model
model = Model()
model_definition = model.model_definition()

from datetime import datetime
import time

def main(args):

    timestamp = datetime.utcnow().isoformat()

    # Get data
    data = args['data']

    # Call the pre-processing step and recieve pre-processed data back
    prepro_start = time.time()
    batch_t = model.preprocess_input(data)
    prepro_time = time.time() - prepro_start

    # Call the predict method using the pre-processed data
    predict_start = time.time()
    prediction = model.predict(model_definition, batch_t)
    predict_time = time.time() - predict_start
    output = {'prediction':prediction}

    out = [timestamp, prepro_time, predict_time, (prepro_time+predict_time)]

    # with open('log.csv', 'a') as file:
    #     file.write(str(out) + '\n')
            
    return {"output": [prediction, out]}
