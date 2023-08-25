# Import the dependencies.
import os
from flask import Flask
import numpy as np
import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import query
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, inspect, MetaData, desc, func
from pathlib import Path
import json


#################################################
# Database Setup
#################################################

# database_path = Path("Resources", "hawaii.sqlite")
detabase_path="C:/Users/Usuario/Butucamopo/Gits Butucamopo/MisterHacker Archivos PC/Challenges en Github/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite"

# database_path = os.path.join('Resources', 'hawaii.sqlite')
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")
print(engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
metadata = MetaData()

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

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
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    
    )
    

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session()
    prcp_results = session.query(measurement.prcp)
    session.close()
    all_prcp = list(np.ravel(prcp_results))
    return jsonify(all_prcp)



if __name__ == "__main__":
    app.run(debug=False)


