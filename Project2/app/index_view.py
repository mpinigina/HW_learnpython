from flask import request, render_template
from app import app, func
import os
import json
import random
import datetime
import numpy as np

def get_random_survey():
    survey = np.array(func.get_survey())
    temp = func.get_temp()
    
    block_total = len(survey)
    block_id = random.randrange(0, block_total)
    finished = 1
    if len(request.args) > 0 and request.args['name'] and request.args['lang']:
        if int(request.args['finished']) > 1 and temp:
            while block_id in temp['finished']:
                block_id = random.randrange(0, block_total)
        finished = int(request.args['finished']) + 1
    result = { 'id': block_id,
               'finished': finished,
               'total': block_total,
               'words': survey[block_id] }
    return result

def temp_to_results():
    results = func.get_results()
    temp = func.get_temp()
    if not temp:
        return
    results.append(temp['result'])
    func.save_results(results)
    func.clear_temp()

def temp_append():
    temp = func.get_temp()
    if not request.args['name'] or not request.args['lang']:
        temp_to_results()
        return
    words = np.array(request.args.getlist('words'))
    translations = np.array(request.args.getlist('translations'))
    commentaries = np.array(request.args.getlist('commentaries'))
    answers = []
    for i in range(0, len(words)):
        answers.append({
            'english': words[i],
            'translation': translations[i],
            'commentary': commentaries[i]
        })
    if int(request.args['finished']) == 1:
        temp = {
            'finished': [ int(request.args['id']) ],
            'result': {
                'name': request.args['name'],
                'language': request.args['lang'],
                'datetime': str(datetime.datetime.today()),
                'answers': answers
            }
        }
    else:
        temp['result']['answers'].extend(answers)
        temp['finished'].append(int(request.args['id']))
    func.save_temp(temp)

@app.route('/index')
@app.route('/')
def findex():
    survey = get_random_survey()
    if len(request.args) == 0 or request.args['finished'] == request.args['total']:
        temp_to_results()
    else:
        temp_append()
    links = func.get_links()
    return render_template("index.html",
                           title="Survey",
                           links=links,
                           survey=survey)