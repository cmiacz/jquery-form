# -*- coding: utf-8 -*-
import datetime
from calendar import monthrange
from flask import Flask, request, render_template

from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, HiddenField, DateTimeField


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["WTF_CSRF_ENABLED"] = False


def get_month_dates():
    try:
        month = datetime.datetime.strptime(request.args.get("month"), "%Y.%m")
    except (TypeError, ValueError):
        month = datetime.datetime.today()

    last = monthrange(month.year, month.month)[1]
    for day in range(1, last + 1):
        yield datetime.date(month.year, month.month, day)


class HiddenDateField(HiddenField):

    def process_formdata(self, valuelist):
        self.data = datetime.datetime.strptime(valuelist[0], "%Y-%m-%d")


class TimeEntryForm(FlaskForm):

    date = HiddenDateField("date")
    time_from = DateTimeField("from", format="%H:%M")
    time_to = DateTimeField("to", format="%H:%M")


class ScheduleForm(FlaskForm):

    time_entries = FieldList(FormField(TimeEntryForm))


@app.route("/")
def root():
    form = ScheduleForm()
    for date in get_month_dates():
        form.time_entries.append_entry({
            "date": date,
            "time_from": datetime.time(hour=8),
            "time_to": datetime.time(hour=16)
        })
    return render_template("index.html", form=form)


@app.route("/schedule", methods=["POST"])
def post_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        for time_entry in form.data["time_entries"]:
            print("{date}: {time_from} - {time_to}".format(**time_entry))
        return render_template("result.html", result="Success")
    return render_template("result.html", result="Failure")


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()
