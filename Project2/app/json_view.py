from app import app, func
import os

@app.route('/json')
def fjson():
    links = func.get_links()
    f = open('app/json/results.json', 'r', encoding='utf8')
    return f.read()