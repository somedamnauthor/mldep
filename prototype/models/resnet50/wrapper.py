from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from resnet50_code import Model
import os
import sys
import time
from datetime import datetime

# Instantiate model
model = Model()
model_definition = model.model_definition()

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def predict():

	timestamp = datetime.utcnow().isoformat()

	if request.method == 'POST':

		# Get data
		data = request.json['data']

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

		with open('log.csv', 'a') as file:
			file.write(str(out) + '\n')
        		
		return output


if __name__ == '__main__':
	app.run(host='0.0.0.0')