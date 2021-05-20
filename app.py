import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

    
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)
    
Measurement = Base.classes.measurement
Station = Base.classes.station
    
session = Session(engine)
    
app = Flask(__name__)
    
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Return the precipitation data from the prior year"""
                       
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()
    
    precip_list = {date: prcp for date, prcp in precip_query}
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def station():
    """Return the stations"""
                       
    stations_list = session.query(Station.station).all()
    stations = list(np.ravel(stations_list))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return tobs for the previous year"""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)
                       
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start, end):
    """Return Temp MIN, Temp AVG, Temp MAX."""

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)

    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps_list = list(np.ravel(results))
    return jsonify(temps_list)


if __name__ == '__main__':
    app.run()

                       