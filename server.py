#!/bin/env python

from flask import Flask, request, abort, make_response, jsonify
import re
app = Flask(__name__)

dict = {}  # carrying url id pairs


def get_key(value):
    for key in dict.keys():
        if str(dict[key]) == value:
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

def check_id(id):
    return int(id) in dict.values()


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def id_handler(id):
    id = str(id) # get rid of the 'u' problem
    if request.method == 'GET':
        url = get_key(id)
        if url:
            return redirect(url, code=301)
        else:
            abort(404)
    if request.method == 'PUT':
        url = check_id(id) and validate_url(str(request.form['url']))
        if url:
            del dict[get_key(id)] # delete old entry
            dict[url] = id #update dict with new url, keep old id
            return make_response('', 200)
        else:
            # There is no url in the request
            # Or id is non-existent
            abort(400)

    if request.method == 'DELETE':
        for key, item in dict.items():
            if str(item) == id:
                del dict[key]
                return ('', 204)
        #item never existed in the first place
        abort(404)


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def url_handler():
    if request.method == 'GET':
        return make_response(jsonify(keys=dict.keys()), 200)
    if request.method == 'POST':
        url = validate_url(str(request.form['url']))
        if url:
            if url in dict.keys():
                return make_response(str(dict[url]), 201)
            else:
                newid = gen_new_id()
                dict[url] = newid
                return make_response(str(dict[url]), 201)
        else:
            abort(400)
    if request.method == 'DELETE':
        dict.clear()
        return ('', 204)

if __name__ == "__main__":
    app.run()
