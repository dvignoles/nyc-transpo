import numpy as np
import pandas as pd
import os, requests
import preprocessing.constants as constants
from preprocessing.common import get_csv_path, clean_column_names
from features.taxi import add_all_features

if os.path.isdir(constants.TAXI_DATA_PATH) is False:
  os.mkdir(constants.TAXI_DATA_PATH)

# store = pd.HDFStore(constants.TAXI_DATA_PATH + '/dataframes.h5')

dtypes = {
    "vendor_id": str,
    "VendorID": str,
    "pickup_datetime": str,
    "dropoff_datetime": str,
    "tpep_pickup_datetime": str,
    "tpep_dropoff_datetime": str,
    "passenger_count": np.int32,
    "trip_distance": np.float32,
    "pickup_longitude": np.float32,
    "pickup_latitude": np.float32,
    "PULocationID": np.int32,
    "DOLocationID": np.int32,
    "rate_code": np.int32,
    "RateCodeID": np.int32,
    "store_and_fwd_flag": str,
    "dropoff_longitude": np.float32,
    "dropoff_latitude": np.float32,
    "payment_type": str,
    "fare_amount": np.float32,
    "surcharge": np.float32,
    "mta_tax": np.float32,
    "tip_amount": np.float32,
    "tolls_amount": np.float32,
    "total_amount": np.float32
}

def get_parsed_df(year, store):
  print("Loading taxi data for year " + year)
  store_key = 'y' + year
  file_path_cleaned = get_csv_path('taxi', year, True)
  file_path_uncleaned = get_csv_path('taxi', year)
  try:
    # See if the store has our data
    stored = store.get(store_key)
    added_new_features = add_all_features(stored, year)
    if added_new_features:
      store[store_key] = stored
      stored.to_csv(file_path_cleaned, index=False)
    return stored
  except KeyError:
    # If not, continue the function below
    pass
  
  # Cleaned is the one-week data with cleaned column names
  # Uncleaned is the full dataset

  cleaned = os.path.isfile(file_path_cleaned)
  if cleaned:
    df_temp = pd.read_csv(file_path_cleaned, dtype=dtypes, na_values='')
  else:
    if os.path.isfile(file_path_uncleaned):
      df_temp = pd.read_csv(file_path_uncleaned, dtype=dtypes, na_values='')
    else:
      print("Stored data not found, downloading...")
      df_temp = pd.read_csv("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_" + year + "-06.csv", dtype=dtypes, na_values='')
    # Standardize the pickup_datetime and dropoff_datetime names
    df_temp.rename(columns={list(df_temp)[1]: 'pickup_datetime'}, inplace = True)
    df_temp.rename(columns={list(df_temp)[2]: 'dropoff_datetime'}, inplace = True)

  # df_temp.sort_values(by=df_temp.columns[1], inplace=True, kind='mergesort')  

  df_temp['pickup_datetime'] = pd.to_datetime(df_temp.iloc[:,1])
  df_temp['dropoff_datetime'] = pd.to_datetime(df_temp.iloc[:,2])
  
  added_new_features = add_all_features(df_temp, year)

  if not cleaned:
    clean_column_names(df_temp)
    # Get only the first week of the month
    df_temp = df_temp.loc[(df_temp['pickup_datetime'] > (year + '-06-01')) & (df_temp['pickup_datetime'] < (year + '-06-08'))]
    # Save the cleaned file
    df_temp.to_csv(file_path_cleaned, index=False)
  elif added_new_features:
    df_temp.to_csv(file_path_cleaned, index=False)

  store[store_key] = df_temp
  return df_temp
