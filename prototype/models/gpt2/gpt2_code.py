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