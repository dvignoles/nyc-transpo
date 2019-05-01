from preprocessing import constants

def clean_column_names(df):
  df.columns = df.columns.str.lstrip().str.replace(' ', '_')

def get_csv_path(data_type, year, processed=False):
    '''determine .csv file name'''
    if data_type is "taxi":
        return constants.TAXI_DATA_PATH + "/" + year + "-06" + ("_parsed_v3" if processed else "") + ".csv"
    elif data_type is "bike":
        return constants.BIKE_DATA_PATH + "/" + year + "-06" + ("_parsed_v3" if processed else "") + ".csv"
    else:
      raise Exception("Data type must be taxi or bike")
