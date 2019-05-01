'''
Data acquisition and cleaning
'''

import pandas as pd
from datetime import datetime
import numpy as np
import requests, zipfile, io, os, re, csv

TAXI_CSV_PATH = "./taxi_data"
BIKE_CSV_PATH = "./bike_data"

# We will use with 2013-2018 June data since June 2013 is when Citi Bike was started, and 2013-2018 data is available for both taxi and bikes.
# We will also filter down to the first week of the month, because the data is an absolute unit
YEARS = ["2013", "2014", "2015", "2016", "2017", "2018"]

def save_csv(file_path, http_data):
    '''write raw request data to .csv'''
    with open(file_path, "w") as f:
      writer = csv.writer(f)
      reader = csv.reader(http_data.text.splitlines())
      for row in reader:
        writer.writerow(row)
        
def get_csv_name(data_type, year, two_weeks_only=False):
    '''determine .csv file name'''
    if data_type is "taxi":
        return TAXI_CSV_PATH + "/" + year + "-06" + ("_parsed_v2" if two_weeks_only is True else "") +  ".csv"
    elif data_type is "bike":
        return BIKE_CSV_PATH + "/" + year + "-06" + ("_parsed_v2" if two_weeks_only is True else "") + ".csv"
    else:
        raise Exception("Data type must be taxi or bike")

def download_taxi():
    '''if taxi data not downloaded, download it'''
    if os.path.isdir(TAXI_CSV_PATH) is False:
        os.mkdir(TAXI_CSV_PATH)

    for n in YEARS:
        file_path = get_csv_name("taxi", n, False)
        if os.path.isfile(file_path) is False:
            data = requests.get("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_" + n + "-06.csv")
            save_csv(file_path, data)


def get_parsed_taxi_df(year):
    dtypes = {
    "vendor_id": "str",
    "VendorID": "str",
    "pickup_datetime": "str",
    "dropoff_datetime": "str",
    "tpep_pickup_datetime": "str",
    "tpep_dropoff_datetime": "str",
    "passenger_count": np.int32,
    "trip_distance": np.float32,
    "pickup_longitude": np.float32,
    "pickup_latitude": np.float32,
    "PULocationID": np.int32,
    "DOLocationID": np.int32,
    "rate_code": np.int32,
    "RateCodeID": np.int32,
    "store_and_fwd_flag": "str",
    "dropoff_longitude": np.float32,
    "dropoff_latitude": np.float32,
    "payment_type": "str",
    "fare_amount": np.float32,
    "surcharge": np.float32,
    "mta_tax": np.float32,
    "tip_amount": np.float32,
    "tolls_amount": np.float32,
    "total_amount": np.float32
    }

  # See if the sorted data was saved before, if so use it
    sorted_file_path = get_csv_name("taxi", year, True)

    if os.path.isfile(sorted_file_path) is True:
        df_toreturn = pd.read_csv(sorted_file_path, dtype=dtypes)
        df_toreturn['pickup_datetime'] = pd.to_datetime(df_toreturn['pickup_datetime'])
        df_toreturn['dropoff_datetime'] = pd.to_datetime(df_toreturn['dropoff_datetime'])
        return df_toreturn

    else:
    # Otherwise, load the full file, sort it, and save it for future reference
        df_temp = pd.read_csv(get_csv_name("taxi", year, False), dtype=dtypes)

        # Standardize the pickup_datetime and dropoff_datetime names
        df_temp.rename(columns = {list(df_temp)[1]: 'pickup_datetime'}, inplace = True)
        df_temp.rename(columns = {list(df_temp)[2]: 'dropoff_datetime'}, inplace = True)

        # Sort by date
        df_temp.sort_values(by=df_temp.columns[1], inplace=True, kind='mergesort')
        df_temp['pickup_datetime'] = pd.to_datetime(df_temp.iloc[:,1])
        df_temp['dropoff_datetime'] = pd.to_datetime(df_temp.iloc[:,2])

        # Get only the first week of the month
        df_temp = df_temp[(df_temp['pickup_datetime'] > (year + '-06-01')) & (df_temp['pickup_datetime'] < (year + '-06-08'))]
        df_temp.to_csv(sorted_file_path, index=False)
        return df_temp

# remove leading whitespace from df_taxi_2014 column names


def clean_col_names(names):
    '''remove leading whitespace + spaces from column names'''
    clean_names = []
    for name in names:
        name = name.lstrip()
        name = name.replace(' ','_')
        clean_names.append(name)
    return(clean_names)
