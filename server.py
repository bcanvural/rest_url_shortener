#!/bin/env python

from flask import Flask, request, abort, make_response, jsonify, redirect
import re
app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 5000

dict = {}  # carrying url id pairs
global id_counter
id_counter = 0


def get_key(value):
    for key, val in dict.items():
        if str(val) == str(value):
            return key
    
    return 0


def gen_new_id():
    global id_counter
    newid = id_counter
    if id_counter < 10:
        id_counter += 1
        return newid
    else:
        return 10


def validate_url(url):
    urls = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    if len(urls) == 1:
        return urls[0]
    else:
        return False

def check_id(id):
    return str(id) in dict.values()


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def id_handler(id):
    id = str(id) # get rid of the 'u' problem
    if request.method == 'GET':
        url = get_key(str(id))
        if url:
            return redirect(url, code=301)
        else:
            return ('', 404)
    
    if request.method == 'PUT':
        url = validate_url(str(request.form['url']))
        if check_id(id) == 0:
            return ('', 404)
        elif url:
            del dict[get_key(str(id))] # delete old entry
            dict[url] = str(id) #update dict with new url, keep old id
            return make_response('', 200)
        else:
            # There is no url in the request
            # Or id is non-existent
            return ('', 400)

    if request.method == 'DELETE':
        for key, item in dict.items():
            if str(item) == id:
                del dict[key]
                return ('', 204)
        #item never existed in the first place
        return ('', 404)


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def url_handler():
    if request.method == 'GET':
        id_list = ""
        for id in dict.values():
            if id_list == "":
                id_list += id
            else:
                id_list += ","+id
        return make_response(id_list, 200)

    if request.method == 'POST':
        url = validate_url(str(request.form['url']))
        if url:
            if url in dict.keys():
                return make_response(str(dict[url]), 201)

            else:
                newid = gen_new_id()
                dict[url] = str(newid)
                return make_response(str(dict[url]), 201)
        else:
            return ('', 400)

    if request.method == 'DELETE':
        dict.clear()
        return ('', 204)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
