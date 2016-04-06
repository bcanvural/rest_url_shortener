#!/bin/env python

from flask import Flask
from flask import request
import re
app = Flask(__name__)

dict = {}  # carrying url id pairs


def get_key(value):
    for key in dict.keys():
        if dict[key] == value:
            return key
        else:
            return False


def gen_new_id():
    return 1


def validate_url(url):
    urls = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    if len(urls) == 1:
        return urls[0]
    else:
        return False


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def id_handler(id):
    if request.method == 'GET':
        url = get_key(id)
        if url:
            return redirect(url, code=301)
        else:
            return "404"
        return id
    if request.method == 'PUT':
        url = validate_url(request.form['url'])
        if url:
            newid = gen_new_id()
            dict[url] = newid
            return
        else:
            # There is no url in the request
            abort(400)

    if request.method == 'DELETE':
        pass


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def url_handler():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        url = validate_url(request.form['url'])
        if url:
            if url in dict.keys():
                return dict[url], 201
            else:
                newid = gen_new_id()
                dict[url] = newid
                return dict[url], 201
        else:
            abort(400)
    if request.method == 'DELETE':
        pass

if __name__ == "__main__":
    app.run()
