import numpy as np
import features.common.zones as zones
from features.common.time import time_to_val

def trip_duration(df, year):
    key = 'tripduration'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df[key] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds()
    return True

def day(df, year):
    key = 'day'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df[key] = df.loc[:,'pickup_datetime'].map(lambda date: int(date.strftime('%d')))
    return True


def zone_from(df, year):
    key = 'zone_from'
    if key in df.columns:
        return False
    if year is '2017' or year is '2018':
        return print("Skipping feature: " + key + " for year " + year + " because of unclean data")
    print("Adding taxi feature: " + key)
    df[key] = np.vectorize(zones.lookup_id)(df.pickup_longitude,df.pickup_latitude)
    df.dropna(subset=[key], inplace=True)
    return True

def zone_to(df, year):
    key = 'zone_to'
    if key in df.columns:
        return False
    if year is '2017' or year is '2018':
        return print("Skipping feature: " + key + " for year " + year + " because of unclean data")
    print("Adding taxi feature: " + key)
    df[key] = np.vectorize(zones.lookup_id)(df.dropoff_longitude,df.dropoff_latitude)
    df.dropna(subset=[key], inplace=True)
    return True
    
def zone_from_to(df, year):
    key = 'zone_from_to'
    if key in df.columns:
        return False
    if year is '2017' or year is '2018':
        return print("Skipping feature: " + key + " for year " + year + " because of unclean data")
    print("Adding taxi feature: " + key)
    df[key] = np.vectorize(zones.from_to)(df.pickup_longitude,df.pickup_latitude,df.dropoff_longitude,df.dropoff_latitude)
    df.dropna(subset=[key], inplace=True)
    return True

def is_bike(df, year):
    key = 'is_bike'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df[key] = 0
    return True

def start_time(df, year):
    key = 'start_time'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df.loc[:,key] = df['pickup_datetime'].apply(lambda x: time_to_val(x.time()))
    return True

def stop_time(df, year):
    key = 'stop_time'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df.loc[:,key] = df['dropoff_datetime'].apply(lambda x: time_to_val(x.time()))
    return True

def add_all_features(df, year):
    new_added = False
    new_added = trip_duration(df, year) or new_added
    new_added = day(df, year) or new_added
    new_added = zone_from(df, year) or new_added
    new_added = zone_to(df, year) or new_added
    new_added = zone_from_to(df, year) or new_added
    new_added = is_bike(df, year) or new_added
    new_added = start_time(df, year) or new_added
    new_added = stop_time(df, year) or new_added
    return new_added


# import numpy as np
# import features.common.zones as zones
# from features.common.time import time_to_val

# def zone_from_to(df, year):
#     values = np.vectorize(zones.from_to_zid)(df['PULocationID'], df['DOLocationID']) if year == '2017' or year == '2018' else np.vectorize(zones.from_to)(df.pickup_longitude,df.pickup_latitude,df.dropoff_longitude,df.dropoff_latitude)
#     df.loc[:, 'zone_from_to'] = values
#     df.drop(df[df['zone_from_to'] == 'nan'].index, inplace=True)
#     return values

# feature_functions = {
#     "trip_duration": lambda df, year: (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds(),
#     "day": lambda df, year: df.loc[:,'pickup_datetime'].map(lambda date: int(date.strftime('%d'))),
#     "zone_from": lambda df, year: df['PULocationID'] if year == '2017' or year == '2018' else np.vectorize(zones.lookup_id)(df.pickup_longitude,df.pickup_latitude),
#     "zone_to": lambda df, year: df['DOLocationID'] if year == '2017' or year == '2018' else np.vectorize(zones.lookup_id)(df.dropoff_longitude,df.dropoff_latitude),
#     "zone_from_to": zone_from_to,
#     "is_bike": lambda df, year: 0,
#     "start_time": lambda df, year: df['pickup_datetime'].apply(lambda x: time_to_val(x.time())),
#     "stop_time": lambda df, year: df['dropoff_datetime'].apply(lambda x: time_to_val(x.time()))
# }

# def add_feature(key, df, year):
#     if key in df.columns:
#         return False
#     if key not in feature_functions:
#         print("Failed to add feature " + key + " because no such function for this feature exists")
#         return False
#     print("Adding taxi feature: " + key)
#     df.loc[:, key] = feature_functions[key](df, year)
#     df.dropna(subset=[key], inplace=True)
#     return True


# def add_all_features(df, year):
#     new_added = False
#     for key in feature_functions:
#         new_added = add_feature(key, df, year) or new_added
#     return new_added
