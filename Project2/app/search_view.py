from flask import request, render_template
from app import app, func
from datetime import datetime, timedelta

@app.route('/search')
def fsearch():
    links = func.get_links()
    dt2 = datetime.today().date()
    dt1 = dt2 - timedelta(days=7)
    return render_template("search.html",
                           title='Search',
                           links=links,
                           dt1=dt1,
                           dt2=dt2)