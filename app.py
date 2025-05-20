
from flask import Flask, render_template, request, redirect, url_for
import markdown2
import random
import util

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", entries=util.list_entries())

@app.route("/wiki/<string:title>")
def entry(title):
    content = util.get_entry(title)
    if content is None:
        return render_template("entry.html", title=title, content=None)
    html = markdown2.markdown(content)
    return render_template("entry.html", title=title, content=html)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if query is None:
        return redirect(url_for('index'))

    entries = util.list_entries()
    matches = [entry for entry in entries if query.lower() in entry.lower()]
    exact_match = util.get_entry(query)

    if exact_match:
        return redirect(url_for('entry', title=query))
    return render_template("search.html", query=query, results=matches)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if util.get_entry(title):
            return render_template("create.html", error="Стаття з такою назвою вже існує.")
        util.save_entry(title, content)
        return redirect(url_for('entry', title=title))
    return render_template("create.html")

@app.route("/edit/<string:title>", methods=["GET", "POST"])
def edit(title):
    if request.method == "POST":
        content = request.form.get("content")
        util.save_entry(title, content)
        return redirect(url_for('entry', title=title))

    content = util.get_entry(title)
    if content is None:
        return render_template("entry.html", title=title, content=None)
    return render_template("edit.html", title=title, content=content)

@app.route("/random")
def random_entry():
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect(url_for('entry', title=title))
