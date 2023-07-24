# Import the dependencies.
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Calculate the date one year from the last date in data set.
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation score
    date_prc = session.query(measurement.date, measurement.prcp)
    date_prc = date_prc.filter(measurement.date >= one_year).all()
    session.close()
    all_dates = []
    for date, prcp in date_prc:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        all_dates.append(precip_dict)
    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
#returning station names
def stations():
    active_station = session.query(station.station).all()
    all_station = list(np.ravel(active_station))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
#returning station names
def tobs():
 
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    most_active = active_station[0][0]
    active_station
    temp_obs = session.query(measurement.tobs).\
    filter((measurement.date >= one_year) & (measurement.station == most_active)).all()
    temp = list(np.ravel(temp_obs))

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start = None, end = None):
    #if no end time specified
    sel = [ 
            func.min(measurement.tobs), 
            func.max(measurement.tobs), 
            func.avg(measurement.tobs)]
    if end == None:
        most_functions = session.query(*sel).\
            filter(measurement.date >= start).all()
        temps = list(np.ravel(most_functions))
        return jsonify(temps)
    
    most_functions1 = session.query(*sel).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    temps1 = list(np.ravel(most_functions1))
    return jsonify(temps1)
    




    


if __name__ == '__main__':
    app.run(debug=True)


