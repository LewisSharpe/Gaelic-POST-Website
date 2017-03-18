#!/usr/bin/env python3
# coding: utf-8

from bottle import Bottle, get, post, run, request, template, static_file, view
import codecs
from POST import GaelicPartOfSpeechTagger, GaelicSentenceSplitter, GaelicTokeniser, tagtext_Default, tagtext_Simplified
import json
import time
from SQLiteLogger import SQLiteLogger
import os
import datetime
import requests
import urllib.parse
from operator import itemgetter
import functools

app = application = Bottle()
gpost = GaelicPartOfSpeechTagger('inputfile', 'outputfile')
tokeniser = GaelicTokeniser()
sentence_splitter = GaelicSentenceSplitter()

logger = SQLiteLogger()

# Credentials for the LocatorHQ API
locator_url = "http://api.locatorhq.com"
api_key = "bf4d582098c3253f7df0ba7c222e833c046d4f4f"
username = "Simon4435"

BASE_URL = "/gaelic/" # Where is the service located

view = functools.partial(view, base_url = BASE_URL)

# Helper to debug 404 - uncomment to catch all routes and output BASE_URL and path 
#@app.get('<mypath:path>')
#def test(mypath):
#    return 'Your path is: %s\nYour baseUrl is %s\n' % (mypath, BASE_URL)	

@app.get(BASE_URL + "static/<filename>")
def get_static(filename):
    return static_file(filename, root="static/")

####################
# REST API methods #
####################

@app.post(BASE_URL + "tokenise/string")
def tokenise():
    """
    Tokenises a text
    Params : text: the text to tokenise
             ip: do we keep the IP adress ? (If param exists, then yes)
             application: the app which issued the request (optional)
    Returns : An array containing the tokens
    """
    time_start = time.time()
    text = request.forms.text
    ip = request.forms.get("ip", None)
    if ip is not None:
        ip = request.environ.get("REMOTE_ADDR")
    
    application = request.forms.get("application", None)

    try:
        tokens = tokeniser.tokenise(text) 
        api_id = logger.log_api_call("/tokenise/string", ip, application)
        text_id = logger.log_text(api_id, text)
        logger.log_tokens(text_id, tokens)

        json_as_string = json.dumps(tokens, ensure_ascii=False)
        logger.log_tokenised_text(text_id, json_as_string)

        time_end = time.time()
        logger.log_api_call_time(api_id, time_end - time_start)
        return json_as_string
    except Exception as e:
        return json.dumps({ 'error': str(e) })


@app.post(BASE_URL + "tokenise/file")
def tokeniseFile():
    """
    Tokenises a file
    Params : file: the file to tokenise (form upload)
             ip: do we keep the IP adress ? (If param exists, then yes)
             application: the app which issued the request (optional)
    Returns : An array containing the tokens
    """
    time_start = time.time()
    f = request.files.get("file")
    ip = request.forms.get("ip", None)
    if ip is not None:
        ip = request.environ.get("REMOTE_ADDR")
    
    application = request.forms.get("application")
    
    timestamp = time.time()
    path = "/tmp/ws-gaelic-%s" % (str(timestamp))
    f.save(path)
    text = gpost.readinputfile(codecs.open(path, "r", "utf-8-sig"))

    try:
        sentences = sentence_splitter.splitsentence(text)
        tokens = []
        for sentence in sentences:
            print(sentence)
            tokens += tokeniser.tokenise(sentence)
            
        api_id = logger.log_api_call("/tokenise/file", ip, application)
        text_id = logger.log_text(api_id, text)
        logger.log_tokens(text_id, tokens)

        json_as_string = json.dumps(tokens, ensure_ascii=False)
        logger.log_tokenised_text(text_id, json_as_string)

        os.remove(path)

        time_end = time.time()
        logger.log_api_call_time(api_id, time_end - time_start)

        return json_as_string
    
    except Exception as e:
        return json.dumps({ 'error': str(e) })

@app.post(BASE_URL + "tag/<method:re:(default|simplified)>/string")
def tag_string(method):
    """
    Tags a text with the Part-Of-Speech Tagger.
    Method can be either "default" or "simplified"
    Params: text: the text to tokenise
            ip: do we keep the IP adress ? (If param exists, then yes)
            application: the name of the application used for the request
    Returns: an array of couples containing the token and its tag
    """
    time_start = time.time()

    text = request.forms.text
    ip = request.forms.get("ip", None)
    if ip is not None:
        ip = request.environ.get("REMOTE_ADDR")

    application = request.forms.get("application")

    print(ip)
    
    try:
        tagged_text = ""
        method_used = ""
        if method == "default":
            tagged_text = tagtext_Default(text)
            method_used = "/tag/default/string"
        elif method == "simplified":
            tagged_text = tagtext_Simplified(text)
            method_used = "/tag/simplified/string"
            
        json_as_string = json.dumps(tagged_text, ensure_ascii=False)
        api_call_id = logger.log_api_call(method_used, ip, application)
        text_id = logger.log_text(api_call_id, text)
        logger.log_tokenised_text(text_id, json_as_string)
        logger.log_tokens(text_id, tagged_text)

        time_end = time.time()
        logger.log_api_call_time(api_call_id, time_end - time_start)
        return json_as_string
    except Exception as e:
        return json.dumps({ 'error': str(e) })

@app.post(BASE_URL + 'tag/<method:re:(default|simplified)>/file')
def tag_file(method):
    """
    Tags a file with the Part-Of-Speech Tagger
    Method can be either "default" or "simplified"
    Params: file: the file to be tagged
            ip: do we keep the IP adress ? (If param exists, then yes)
            application: the application used to issue the request
    Returns: an array containing couples with token / tag
    """
    time_start = time.time()
    
    f = request.files.get("file")
    ip = request.forms.get("ip", None)
    if ip is not None:
        ip = request.environ.get("REMOTE_ADDR")
        
    application = request.forms.get("application")
    
    timestamp = time.time()
    path = "/tmp/ws-gaelic-%s" % (str(timestamp))
    f.save(path)
    text = gpost.readinputfile(codecs.open(path, "r", "utf-8-sig"))

    try:
        os.remove(path)
        
        tagged_text = ""
        method_used = ""
        if method == "default":
            tagged_text = tagtext_Default(text)
            method_used = "/tag/default/file"
        elif method == "simplified":
            tagged_text = tagtext_Simplified(text)
            method_used = "/tag/simplified/file"

        json_as_text = json.dumps(tagged_text, ensure_ascii=False)
        api_call_id = logger.log_api_call(method_used, ip, application)
        text_id = logger.log_text(api_call_id, text)
        logger.log_tokenised_text(text_id, json_as_text)
        logger.log_tokens(text_id, tagged_text)

        time_end = time.time()
        logger.log_api_call_time(api_call_id, time_end - time_start)
            
        return json_as_text
    except Exception as e:
        return json.dumps({ 'error': str(e) })

#############
# Info page #
#############

@app.get(BASE_URL)
@view("home")
def home():
    return

@app.get(BASE_URL + "howitworks")
@view("howitworks")
def howitworks_function():
    return

@app.get(BASE_URL + "tokeniser")
@view("tokeniser")
def tokeniser_function():
    return

@app.get(BASE_URL + "tagger")
@view("tagger")
def tagger_function():
    return

@app.get(BASE_URL + "no_file_uploaded")
@view("no_file_uploaded")
def no_file_uploaded_function():
    return

@app.get(BASE_URL + "about")
@view("about")
def about():
    return

@app.get(BASE_URL + "doc")
@view("doc")
def doc():
    return

@app.get(BASE_URL + "contact")
@view("contact")
def contact():
    return

@app.get(BASE_URL + "demos")
@view("demos")
def demos():
    return

@app.get(BASE_URL + "infos")
def infos():
    try:
        return template("infos_template", nb_calls = len(logger.get_api_calls()),
                        nb_unique_tokens = len(logger.get_unique_tokens()),
                        base_url=BASE_URL) 
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/api_calls")
def infos_api_calls():
    try:
        return template("api_calls", api_calls = logger.get_api_calls(), base_url=BASE_URL)
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/api_calls/<call_id>")
def infos_api_call_id(call_id):
    try:
        return template("api_call_id", api_call=logger.get_api_call_id(call_id), base_url=BASE_URL)
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/api_calls/by_ip/<ip>")
def infos_calls_by_ip(ip):
    try:
        all_calls = logger.get_api_calls()
        ip_calls = [c for c in all_calls if c[2] == ip]

        return template("api_calls", api_calls=ip_calls, base_url=BASE_URL)
        
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/ip/<ip>")
def infos_ip(ip):
    try:
        r = requests.get(locator_url, params={ 'key': api_key,
                                               'user': username,
                                               'format': 'json',
                                               'ip': ip})
        location = r.json()
        return template("ip_infos", ip=ip,
                        lat=location["latitude"],
                        long=location["longitude"],
                        country=location["countryName"],
                        base_url=BASE_URL)
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/tokens")
def infos_tokens():
    try:
        tokens=logger.get_unique_tokens()
        total_tokens = 0;
        for t in tokens:
            total_tokens += t[1] # t[1] is the result of count

        tokens = sorted(tokens, key=itemgetter(1), reverse=True)
        
        return template("tokens", tokens=tokens, total=total_tokens, base_url=BASE_URL, urlencode=urllib.parse.urlencode)
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/token")
def infos_token():
    try:
        token = request.query.token
        tags = logger.get_tags_for_token(token)
        return template("token_infos", token=token, tags=tags, base_url=BASE_URL)
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)    
    
@app.get(BASE_URL + "infos/map")
def infos_map():
    try:
        ips = logger.get_unique_ips()
        final_result = []
        for ip_and_count in ips:
            if ip_and_count[0] is not None:
                final_result.append( (ip_and_count[0].strip(), ip_and_count[1]) )
                
        return template("map", ips=final_result, base_url=BASE_URL)
        
    except Exception as e:
        return template("error", error=str(e), base_url=BASE_URL)

@app.get(BASE_URL + "infos/get_location_from_ip/<ip>")
def get_location_from_ip(ip):
    r = requests.get(locator_url, params={ 'key': api_key,
                                           'user': username,
                                           'format': 'json',
                                           'ip': ip})
    try:
        location = r.json()
        return json.dumps( { 'ip': ip,
                             'latitude': location['latitude'],
                             'longitude': location['longitude'] })
    except ValueError as ve:
        json.dumps({'error': 'Not found'})
    
if __name__ == "__main__":
    app.run(host="localhost", port=9092, reloader=True, debug=True)
