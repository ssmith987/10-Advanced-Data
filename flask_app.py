# import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
import pandas as pd

#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).\
                filter(Measurement.date <= last_date).\
                order_by(Measurement.date).all()

    prcp_totals = []
    for result in year_precip:
        row = {}
        row["date"] = result.date
        row["prcp"] = result.prcp
        prcp_totals.append(row)

    return jsonify(prcp_totals)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station, Station.name).all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= first_date).all()
    temp_obs = []
    for temp in temps:
        row = {}
        row["date"] = temp.date
        row["tobs"] = temp.tobs
        temp_obs.append(row)

    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)


