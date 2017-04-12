#!/usr/bin/env python2
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from spectrogram import Spectrogram
import os

app = Flask(__name__)
api = Api(app)

api.add_resource(Spectrogram, '/spectrogram/<string:title>')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/')
def test_html():
    titles = [ s[:-4] for s in os.listdir('./static') if s[-4:]=='.wav']
    return render_template('index.html', titles=titles)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
