#!/bin/env python

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def id_handler(id):
    if request.method == 'GET':
        return id
    if request.method == 'PUT':
        print request.form['payload']
        return
    if request.method == 'DELETE':
        pass

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def url_handler():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        return request.form['url']
        return "200"
    if request.method == 'DELETE':
        pass

if __name__ == "__main__":
    app.run()




