from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about(name = None):
    return render_template("about.html")

@app.route("/convert")
def convert():
    return render_template("convert.html")