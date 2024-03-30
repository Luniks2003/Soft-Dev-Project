from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
@app.route("/about/<name>")
def about(name = None):
    return render_template("about.html", name = name)

@app.route("/upload")
def upload():
    return "upload file here"