import numpy as np
import pandas as pd
import os, zipfile, requests, re, io
from preprocessing.common import get_csv_path, clean_column_names
from preprocessing import constants
from features.bike import add_all_features

if os.path.isdir(constants.BIKE_DATA_PATH) is False:
  os.mkdir(constants.BIKE_DATA_PATH)

dtypes = {
    "tripduration": np.int32,
    "starttime": object,
    "stoptime": object,
    "start station id": np.float32,
    "start station name": object,
    "start station latitude": np.float32,
    "start station longitude": np.float32,
    "end station id": np.float32,
    "end station name": object,
    "end station latitude": np.float32,
    "end station longitude": np.float32,
    "bikeid": np.int32,
    "usertype": object,
    "birth year": np.float32,
    "gender": np.int32
}


def get_date_format(year):
  if year is '2015':
    return '%m/%d/%Y %H:%M'
  elif year is '2016':
    return '%m/%d/%Y %H:%M:%S'
  elif year is '2017':
    return '%Y-%m-%d %H:%M:%S'
  elif year is '2018':
    return '%Y-%m-%d %H:%M:%S'
  else:
    return ''

# Since Citi Bike does not directly provide csv files, we must handle the zip files, extract, and load them accordingly. 
def get_parsed_df(year, store):
  print("Loading bike data for year " + year)
  store_key = 'y' + year
  file_path_cleaned = get_csv_path('bike', year, True)
  file_path_uncleaned = get_csv_path('bike', year)
  try:
    stored = store[store_key]
    added_new_features = add_all_features(stored, year)
    if added_new_features:
      store[store_key] = stored
      stored.to_csv(file_path_cleaned, index=False)
    return stored
  except KeyError:
    pass

  na_values = '\\N'

  cleaned = os.path.isfile(file_path_cleaned)
  
  if cleaned:
    df_temp = pd.read_csv(file_path_cleaned, dtype=dtypes, na_values=na_values)
  else:
    if os.path.isfile(file_path_uncleaned):
      df_temp = pd.read_csv(file_path_uncleaned, dtype=dtypes, na_values=na_values)
    else:
      # Request the ZIP and get the file contents
      print("Stored data not found, downloading...")
      req_url = "https://s3.amazonaws.com/tripdata/" + year + ("06-citibike-tripdata.csv.zip" if year is '2017' or year is '2018' else "06-citibike-tripdata.zip")
      z = zipfile.ZipFile(io.BytesIO(requests.get(req_url).content))
      orig_file_name = list(filter(re.compile("^\d+.*\.csv$").match, z.namelist()))[0]

      # Extract it and move it to the appropriate folder
      z.extract(orig_file_name)
      os.rename(orig_file_name, file_path_uncleaned) # Renaming the file will automatically remove the original, extracted file
      
      df_temp = pd.read_csv(file_path_uncleaned, dtype=dtypes, na_values=na_values)

  # Convert to datetime
  df_temp['starttime'] = pd.to_datetime(df_temp['starttime'], format=get_date_format(year) if not cleaned else '')
  df_temp['stoptime'] = pd.to_datetime(df_temp['stoptime'], format=get_date_format(year) if not cleaned else '')
  
  added_new_features = add_all_features(df_temp, year)

  if not cleaned:
    clean_column_names(df_temp)
    # Limit the dataset to 1 week of June 
    df_temp = df_temp.loc[(df_temp['starttime'] > year + '-06-01') & (df_temp['starttime'] < year + '-06-08')]
    # Save the cleaned file
    df_temp.to_csv(file_path_cleaned, index=False)
  elif added_new_features:
    df_temp.to_csv(file_path_cleaned, index=False)
  
  store[store_key] = df_temp
  
  return df_temp
