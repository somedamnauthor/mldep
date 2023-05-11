from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from alexnet_code import Model
import os
import sys

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def predict():

	if request.method == 'POST':
		data_path = request.form['data_path']
		classes_path = request.form['classes_path']

		model = Model()

		model_definition = model.model_definition()
		batch_t = model.preprocess_input(data_path)
		prediction = model.predict(model_definition, batch_t, classes_path)

		output = {'prediction':prediction}

		return output


if __name__ == '__main__':
	app.run(host='0.0.0.0')

