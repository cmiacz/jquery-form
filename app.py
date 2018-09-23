# -*- coding: utf-8 -*-
import datetime

from calendar import monthrange
from flask import Flask, request, render_template


app = Flask(__name__)
app.config["DEBUG"] = True


def get_dates(month):
    last = monthrange(month.year, month.month)[1]
    for day in range(1, last + 1):
        yield datetime.date(month.year, month.month, day)


@app.route("/")
def root():
    month = request.args.get("month")
    try:
        month = datetime.datetime.strptime(month, "%Y.%m")
    except (TypeError, ValueError):
        month = datetime.datetime.today()
    return render_template("index.html", dates=get_dates(month))


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


@app.route('/schedule', methods=['POST'])
def transcribe():
    print(request.json)
    return "OK"


if __name__ == "__main__":
    app.run()
