from web.apps.web import web_bp as app
from flask import render_template, render_template


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")
