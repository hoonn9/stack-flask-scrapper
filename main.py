from flask import Flask, render_template, request, redirect
from scrapper import get_so_jobs

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_so_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs=jobs)

# @app.route("/<username>")
# def contact(username):
#     return f"<h1>Hello your name is {username}</h1>"


app.run(host="127.0.0.1")
