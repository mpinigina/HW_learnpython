from flask import request, render_template
from app import app, func
from datetime import datetime

def get_filter_results():
    lang = request.args['lang']
    dt1 = request.args['dt1']
    dt2 = request.args['dt2']
    if dt1:
        dt1 = datetime.strptime(dt1, '%Y-%m-%d')
    if dt2:
        dt2 = datetime.strptime(dt2, '%Y-%m-%d')
    all_results = func.get_results()
    results = []
    for result in all_results:
        cur_dt = datetime.strptime(result['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        cur_lang = result['language']
        if (lang and cur_lang.find(lang) == -1 or
            dt1 and cur_dt.date() < dt1.date() or
            dt2 and cur_dt.date() > dt2.date()):
            continue
        result['datetime'] = cur_dt.strftime('%d.%m.%Y %H:%M:%S')
        results.append(result)
    return results

@app.route('/results')
def fresults():
    results = get_filter_results()
    links = func.get_links()
    return render_template("results.html",
                           title='Results',
                           links=links,
                           results=results)
