import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    sel = [Measurement.date,Measurement.prcp]
    queryresult = session.query(*sel).all()
    session.close()

    precipitation = []
    for date, prcp in queryresult:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = {}
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name
    session.close()
    return jsonify(stations)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

def tobs():
    session = Session(engine)

# Last Year of Data   
    latestdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    oneyearprior = dt.datetime.strptime(lateststr[0], '%Y-%m-%d')
    querydate = dt.date(oneyearprior.year -1, oneyearprior.month, oneyearprior.day)

# Most Active Station
    stations = [measurement.station,func.count(measurement.id)]
    stationsort = session.query(stations).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()

# 12-month data for most active station
    sel = [Measurement.date,Measurement.tobs]
    query = session.query(measurement.date,measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= querydate).all()

    tobsall = []
    for date, tobs in query:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)
    return jsonify(tobsall)

    session.close()

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive

@app.route("/api/v1.0/<start>")
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobs_list = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Avg"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def get_t_start_end(start,end):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Avg"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)
    return jsonify(tobs)

    ### Flask End###

if __name__ == '__main__':
    app.run(debug=True)

