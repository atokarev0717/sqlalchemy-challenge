import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

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

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Home page<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """all precipitation results available in the dataset"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # pull all precipitation results available in the dataset
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value
    all_precipitation = []
    for date, precipitation in prcp_query:
        precipitation_dict = {}
        precipitation_dict[date] = precipitation
        all_precipitation.append(precipitation_dict)

    # convert the df into JSON format and return to the client
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """list of all stations in the data set"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of stations from the dataset
    stations_query = session.query(Station.station, Station.name).all()

    all_stations = []
    for station, name in stations_query:
        station_dict = {}
        station_dict[station] = name
        all_stations.append(station_dict)
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """temperature observations of the most active station for the last year of data"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    
    the_most_active_station = most_active_stations[0][0]
    query_date = dt.date(2016,8 ,23)

    #Query the dates and temperature observations of the most active station for the last year of data
    the_most_active_station_data =  session.query(Measurement.date,Measurement.tobs).\
                    filter(Measurement.station == the_most_active_station).\
                    filter(Measurement.date >= query_date).all()

    lastyear_tobs= []
    for date, tobs in the_most_active_station_data:
        tobs_dict = {}
        tobs_dict[date] = tobs
        lastyear_tobs.append(tobs_dict)
    
    return jsonify(lastyear_tobs)

@app.route("/api/v1.0/<start>")
def temp_start_date(start):
    """ Takes Start Date and returns `TMIN`, `TAVG`, and `TMAX` 
    for all dates greater than and equal to the start date """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_start_date_query = session.query(Measurement.date,\
                                func.min(Measurement.tobs),\
                                func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()
    
    temp_start_date_lst = []

    for date, TMIN, TAVG, TMAX in temp_start_date_query:
        temp_start_date_dict = {}
        temp_start_date_dict['date'] = date
        temp_start_date_dict['TMIN'] = TMIN
        temp_start_date_dict['TAVG'] = TAVG
        temp_start_date_dict['TMAX'] = TMAX
        temp_start_date_lst.append(temp_start_date_dict)
    
    return jsonify(temp_start_date_lst)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end_date(start, end):
    """ Takes Start Date, End Date and returns `TMIN`, `TAVG`, 
    and `TMAX` for dates between the start and end date inclusive """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_start_end_date_query = session.query(Measurement.date,\
                                func.min(Measurement.tobs),\
                                func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start, Measurement.date <= end).\
                        group_by(Measurement.date).all()
    
    temp_start_date_lst = []

    for date, TMIN, TAVG, TMAX in temp_start_end_date_query:
        temp_start_date_dict = {}
        temp_start_date_dict['date'] = date
        temp_start_date_dict['TMIN'] = TMIN
        temp_start_date_dict['TAVG'] = TAVG
        temp_start_date_dict['TMAX'] = TMAX
        temp_start_date_lst.append(temp_start_date_dict)
    
    return jsonify(temp_start_date_lst)


if __name__ == '__main__':
    app.run(debug=True)
