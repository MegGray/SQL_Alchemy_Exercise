from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# @author: Megan Gray
# @date: 2018-11-10
# Unit 10 Homework
#################################################


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return (
        f"Welcome to the Weather Station API for Hawaii!<br/>"
        f"Compiled by Megan Gray<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>"
    )

# Precipitation Data
@app.route("/api/v1.0/precipitation")
def preciptiation():
    """Return the precipitation data as json"""
    # Query results to retrieve dates and total precipitation for each station
    precip = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    
    # Convert list of tuples into normal list
    precipitation = list(np.ravel(precip))

    return jsonify(precipitation)


# Stations Data
@app.route("/api/v1.0/stations")
def stations():
    """Return the station data as json"""
    station_data = session.query(Station.id, Station.name, Station.station).\
        order_by(Station.id).all()
    # Convert list of tuples into normal list
    stations = list(np.ravel(station_data))
    #   * Return a JSON list of stations from the dataset.
    return jsonify(stations)

# Temperature Data
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data as json"""
    #   * query for the dates and temperature observations from a year from the last data point.    
    temperature = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert list of tuples into normal list
    temp_year = list(np.ravel(temperature))

    #   * Return a JSON list of Temperature Observations (tobs) for the previous year.  
    return jsonify(temp_year)


#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/temp/<start>")
def start(start=None):
    """Return the start of vacation data as json"""
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_results = list(np.ravel(start_date))
    #   * Return a JSON list of `TMIN`, `TAVG`, and `TMAX` for all observations
    return jsonify(start_results)

@app.route("/api/v1.0/temp/<start>/<end>")
def calc_temps(start,end):
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    dates_results = list(np.ravel(results))

    # return data as json.
    return jsonify(dates_results) 

if __name__ == "__main__":
    app.run(debug=True)
