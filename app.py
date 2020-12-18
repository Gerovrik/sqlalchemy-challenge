#base template imported from Gitlab activites week 10

from flask import Flask, jsonify
import datetime as dt
import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
##################################################################################################
# Flask Setup
##################################################################################################
app = Flask(__name__)


##################################################################################################
#Flask Routes
##################################################################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/ and /api/v1.0//<br/>"
    )
##################################################################################################

##################################################################################################
@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of rain fall for previous year"""

    # Create our session (link) from Python to the DB
    # pulled directily from Climate_starter.ipynb file
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    previous_year= dt.datetime.strptime(date, '%Y-%m-%d') - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= previous_year).order_by(Measurement.date).all()

    #Created a Dictionary for precipitation 
    precipitation_dict= dict(precipitation)
  
    return jsonify(precipitation_dict)
##################################################################################################

##################################################################################################
@app.route("/api/v1.0/stations")
def stations():
    """Returns a Json list of the stations from data"""

    Stations_query = session.query(Measurement.station).group_by(Measurement.station).all()

    Stations_list = list(np.ravel(Stations_query))

    return jsonify(Stations_list)
##################################################################################################

##################################################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a Json list of temperatures for previous year"""

    tobs_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    tobs_year = dt.datetime.strptime(tobs_date, '%Y-%m-%d') - dt.timedelta(days=365)

    tobs_list = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= tobs_year)\
        .order_by(Measurement.date).all()


    return jsonify(tobs_list)
##################################################################################################

##################################################################################################
@app.route("/api/v1.0/<start>")
def Temp_start(start=None):
    """Returns a Json list of TMIN,TAVG, TMAX for all dates greater than and equal to the start date"""

    Temp_start_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()

    Temp_start_list=list(Temp_start_query)

    return jsonify(Temp_start_list)
##################################################################################################

##################################################################################################
@app.route("/api/v1.0/<start>/<end>")
def Temp_start_end(start=None, end=None):
    """Returns a Json list of TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""

    Temp_end_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    Temp_end_list = list(Temp_end_query)

    return jsonify(Temp_end_list)
##################################################################################################

##################################################################################################



if __name__ == '__main__':
    app.run(debug=True)
