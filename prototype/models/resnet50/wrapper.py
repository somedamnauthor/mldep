from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from resnet50_code import Model
import os
import sys

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def predict():

	if request.method == 'POST':

		# Get data
		data = request.form['data']

		# Instantiate model
		model = Model()
		model_definition = model.model_definition()

		# Call the pre-processing step and recieve pre-processed data back
		batch_t = model.preprocess_input(data)

		# Call the predict method using the pre-processed data
		prediction = model.predict(model_definition, batch_t)
		output = {'prediction':prediction}

		return output


if __name__ == '__main__':
	app.run(host='0.0.0.0')

