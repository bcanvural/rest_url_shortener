#!/bin/env python

from flask import Flask, request, abort, make_response, jsonify, redirect
import re
app = Flask(__name__)

dict = {}  # carrying url id pairs
# id_counter = 65
global id_counter
id_counter = 0
id_char_num = 1


def get_key(value):
    # print "get_key: " + str(dict.items())
    # print str(value)
    for key, val in dict.items():
        # if str(dict[key]) == str(value):
        # print str(val) + " == " + str(value)
        if str(val) == str(value):
            return key
    
    return 0


def gen_new_id():
    global id_counter
    newid = id_counter
    # if id_counter < 91:
    #     id_counter += 1
    #     return chr(id)
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
        # print url
        if url:
            return redirect(url, code=301)
        else:
            return ('', 404)
            # abort(404) # causes 233 char body which ruby client doesnt want
    if request.method == 'PUT':
        url = validate_url(str(request.form['url']))
        # if id not in dict.viewvalues():
            # print dict.viewvalues()
        if check_id(id) == 0:
            # print "id not found"
            return ('', 404)
            # abort(404) # causes 233 char body which ruby client doesnt want
        elif url:
            del dict[get_key(str(id))] # delete old entry
            dict[url] = str(id) #update dict with new url, keep old id
            return make_response('', 200)
        else:
            # There is no url in the request
            # Or id is non-existent
            return ('', 400)
            # abort(400) # causes 233 char body which ruby client doesnt want

    if request.method == 'DELETE':
        for key, item in dict.items():
            if str(item) == id:
                del dict[key]
                return ('', 204)
        #item never existed in the first place
        return ('', 404)
        # abort(404) # causes 233 char body which ruby client doesnt want


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def url_handler():
    if request.method == 'GET':
        # print jsonify(keys=dict.keys())
        # print str(dict.keys())
        # print dict.items()
        id_list = ""
        for id in dict.values():
            if id_list == "":
                id_list += id
            else:
                id_list += ","+id
        # print id_list
        return make_response(id_list, 200)
        # return make_response(str(dict.keys()), 200)
        # return make_response(jsonify(keys=dict.keys()), 200)
    if request.method == 'POST':
        # print dict.keys()
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
            # abort(400) # causes 233 char body which ruby client doesnt want
    if request.method == 'DELETE':
        dict.clear()
        return ('', 204)

if __name__ == "__main__":
    app.run()
