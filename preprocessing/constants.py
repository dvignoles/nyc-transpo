# We will use with 2013-2018 June data since June 2013 is when Citi Bike was started, and 2013-2018 data is available for both taxi and bikes.
# We will also filter down to the first week of the month, because the data is an absolute unit
YEARS = ["2013", "2014", "2015", "2016", "2017", "2018"]

TAXI_DATA_PATH = "./taxi_data"
BIKE_DATA_PATH = "./bike_data"

ZONES = [] # List of all Zone objects 
ZONES_DIC = {} # Dictionary of all zones with location_id as key
