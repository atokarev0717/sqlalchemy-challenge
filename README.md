# sqlalchemy-challenge

## Step 1 - Climate Analysis and Exploration

Step1 uses Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. The resukts can be viewed in the [jupyter notebook](./climate_alchemy.ipynb)

There are two parts of the analysis **Precipitation Analysis** and **Station Analysis**

## Step 2 - Climate App

Step 2 is to develop a Flask API based on the queries that have been just developed in Step1
#### Available routes

`/` - Home Page. it lists all routes that are available

`/api/v1.0/precipitation` - Returns ALL precipitation measurements in JSON format

`/api/v1.0/stations` - Returns a JSON list of stations from the dataset.

`/api/v1.0/tobs` - Returns a JSON list of dates and temperature observations of the most active station for the last year of data.

`/api/v1.0/<start>` - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date

`/api/v1.0/<start>/<end>` - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a range of given start and end date



