# Imports

import base64
from io import BytesIO
import re

# import torch

import os
import sys
import warnings
warnings.filterwarnings("ignore")

from transformers import GPT2LMHeadModel, GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set temperature and top-k parameters
temperature = 0.3  # Adjust this value to control the randomness of the output
top_k = 50  # Adjust this value to limit the number of next tokens considered

class Model:

    def model_definition(self):

        GPT2 = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

        return GPT2


    def preprocess_input(self, data):

        # encode context the generation is conditioned on
        input_ids = tokenizer.encode(data, return_tensors='pt')
     
        return input_ids


    def predict(self, model, batch_t):

        # generate text until the output length (which includes the context length) reaches 50
        # greedy_output = model.generate(batch_t, max_length = MAX_LEN)

        # Generate text with the model
        greedy_output = model.generate(
            batch_t,
            max_length=50,  # Adjust the maximum length of the generated text
            num_return_sequences=1,
            temperature=temperature,
            top_k=top_k,
            )

        # print("Output:\n" + 100 * '-')
        prediction = tokenizer.decode(greedy_output[0], skip_special_tokens = True)

        return prediction

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
