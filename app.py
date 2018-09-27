# -*- coding: utf-8 -*-
import datetime
from dateutil import relativedelta
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
    try:
        current_month = datetime.datetime.strptime(request.args.get("month"), "%Y.%m")
    except (TypeError, ValueError):
        current_month = datetime.datetime.today()

    return render_template(
        "index.html",
        dates=get_dates(current_month),
        prev_month=current_month - relativedelta.relativedelta(months=1),
        next_month=current_month + relativedelta.relativedelta(months=1),
    )


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


@app.route('/schedule', methods=['POST'])
def post_schedule():
    data = request.json
    for date, time in data.items():
        print("{}: {} - {}".format(date, time["from"], time["to"]))
    return "OK"


if __name__ == "__main__":
    app.run()
