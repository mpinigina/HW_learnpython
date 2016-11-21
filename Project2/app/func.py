from flask import url_for
import os
import json

def get_links():
    links = {
        'index': url_for('findex'),
        'stats': url_for('fstats'),
        'json': url_for('fjson'),
        'search': url_for('fsearch'),
        'results': url_for('fresults')
    }
    return links

def get_survey():
    survey = json_to_list('app/json/survey.json')
    return survey

def get_results():
    results = json_to_list('app/json/results.json')
    return results

def save_results(data):
    list_to_json(data, 'app/json/results.json')

def get_temp():
    temp = json_to_list('app/json/temp.json')
    return temp

def save_temp(data):
    list_to_json(data, 'app/json/temp.json')

def clear_temp():
    f = open('app/json/temp.json', 'w', encoding='utf8')
    f.write('')

def json_to_list(data, from_file = True):
    result = ''
    if from_file:
        json_str = open(data, 'r', encoding='utf8').read()
        if json_str:
            result = json.loads(json_str)
        else:
            result = []
    else:
        result = json.loads(data)
    return result

def list_to_json(data, file_path = ''):
    result = json.dumps(data)
    if file_path:
        f = open(file_path, 'w', encoding='utf8')
        f.write(result)
    return result