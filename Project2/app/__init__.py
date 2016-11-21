from flask import Flask, url_for

app = Flask(__name__)

from app import index_view, stats_view, json_view, search_view, results_view

@app.route('/functions/<fname>')
def f_address(fname):
    return 'The address for %s is %s' % (fname, url_for(fname))