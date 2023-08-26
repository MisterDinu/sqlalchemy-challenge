# Import the dependencies.
from flask import Flask
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import query
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, inspect, MetaData, desc, func
from pathlib import Path
from flask import jsonify


#################################################
# Database Setup
#################################################

database_path = Path("Resources", "hawaii.sqlite")
engine = create_engine(f"sqlite:///{database_path}")
print(engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
metadata = MetaData()

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

most_repeated_id = "USC00519281"

# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)

#################################################
# Flask Setup
#################################################

app= Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        "Welcome to homepage, these are the available routes:<br/>"
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start> (specify the start date after v1.0/, in format: %Y-%m-%d)<br/>'
        f'/api/v1.0/<start>/<end> (after v1.0/, specify the start date, then, after the other "/", specify the end date, in format: %Y-%m-%d)'
    )
    
# Just for last year


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session()
    latest_date = session.query(func.max(measurement.date)).scalar() 
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    start_date = latest_date - timedelta(days=365)
    prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date)
    session.close()
    prcp_list = []
    for result in prcp_results:
        prcp_dict ={
            result[0]:result[1]
        }
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session()
    stations = session.query(station).all()
    stations_list = []
    for st in stations:
        station_dict = {
            "Station ID":st.station,
            "Station name":st.name
        }
        stations_list.append(station_dict)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session()
    latest_date = session.query(func.max(measurement.date)).scalar() 
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    start_date = latest_date - timedelta(days=365)
    most_repeated_tobs = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= start_date).\
        filter(measurement.station == most_repeated_id)
    session.close()
    tobs_list = []
    for tob in most_repeated_tobs:
        tobs_dict ={
            "Date":tob[0],
            "Temperature(F)":tob[1]
        }
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session()
    retrieved_date_temps = session.query(measurement.tobs).\
        filter(measurement.date >= start)
    session.close()
    date_tobs_list = []
    for tob in retrieved_date_temps:
        date_tobs_list.append(tob[0])
    max_temp = max(date_tobs_list)
    min_temp = min(date_tobs_list)
    avg_temp = sum(date_tobs_list)/len(date_tobs_list)
    # return f'Retrieved date: {date_tobs_list}'
    return f'''
    Retrieved date: {start}<br/>
    Max temperature: {max_temp}<br/>
    Min temperature: {min_temp}<br/>
    Average temperature: {round(avg_temp, 3)}
    '''

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end): 
    session = Session()
    retrieved_range_temps = session.query(measurement.tobs).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end)
    session.close()
    range_tobs_list = []
    for tob in retrieved_range_temps:
        range_tobs_list.append(tob[0])
    max_temp = max(range_tobs_list)
    min_temp = min(range_tobs_list)
    avg_temp = sum(range_tobs_list)/len(range_tobs_list)
    # return f'Retrieved date: {range_tobs_list}'
    return f'''
    Retrieved date: {start}<br/>
    Max temperature: {max_temp}<br/>
    Min temperature: {min_temp}<br/>
    Average temperature: {round(avg_temp, 3)}
    '''


if __name__ == "__main__":
    app.run(debug=True)



