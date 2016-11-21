from flask import render_template
from app import app, func
import numpy as np
from datetime import datetime

def get_most_pop_lang(results):
    langs = {}
    for result in results:
        lang = result['language']
        if lang in langs:
            langs[lang] += 1
        else:
            langs[lang] = 1
    most_pop_lang = {}
    for lang, count in langs.items():
        if not most_pop_lang:
            most_pop_lang = {
                'lang': lang,
                'count': count
            }
        else:
            if count > most_pop_lang['count']:
                most_pop_lang = {
                    'lang': lang,
                    'count': count
                }
    return most_pop_lang

def get_dates(results):
    dates = {}
    for result in results:
        dt = datetime.strptime(result['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        dt_str = dt.strftime('%d.%m.%Y')
        if dt_str in dates:
            dates[dt_str] += 1
        else:
            dates[dt_str] = 1
    return dates

def get_quest_count(survey):
    quest_count = 0
    for block in survey:
        quest_count += len(block)
    print(quest_count)
    return quest_count

def get_stats():
    results = np.array(func.get_results())
    survey = func.get_survey()
    quest_count = get_quest_count(survey)
    most_pop_lang = get_most_pop_lang(results)
    dates = get_dates(results)
    stats = {
        'quest_count': quest_count,
        'iv_count': len(results),
        'most_pop_lang': most_pop_lang,
        'dates': dates
    }
    return stats

@app.route('/stats')
def fstats():
    stats = get_stats()
    links = func.get_links()
    return render_template("stats.html",
                           title='Stats',
                           links=links,
                           stats=stats)
