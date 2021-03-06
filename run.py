#!/usr/bin/env python2

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from results import Results, get_suggestions
import os


app = Flask(__name__, template_folder='./static')
api = Api(app)

api.add_resource(Results, '/results/')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # Only need POST requests
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route('/')
def render_html():
    return render_template('index.html', suggestions=get_suggestions())

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0',debug=False, threaded=True, port=port)
