import numpy as np
import features.common.zones as zones
from features.common.time import time_to_val

def trip_distance(df, year):
    key = 'trip_distance'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df[key] = zones.haversine(
    df['start_station_latitude'], 
    df['start_station_longitude'],
    df['end_station_latitude'], 
    df['end_station_longitude'])
    return True

def day(df, year):
    key = 'day'
    if key in df.columns:
        return False
    print("Adding taxi feature: " + key)
    df[key] = df.loc[:,'starttime'].map(lambda date: int(date.strftime('%d')))
    return True

def zone_from(df, year):
    key = 'zone_from'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df[key] = np.vectorize(zones.lookup_id)(df.start_station_longitude, df.start_station_latitude)
    df.dropna(subset=[key], inplace=True)
    return True

def zone_to(df, year):
    key = 'zone_to'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df[key] = np.vectorize(zones.lookup_id)(df.end_station_longitude, df.end_station_latitude)
    df.dropna(subset=[key], inplace=True)
    return True
    
def zone_from_to(df, year):
    key = 'zone_from_to'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df[key] = np.vectorize(zones.from_to)(df.start_station_longitude, df.start_station_latitude, df.end_station_longitude, df.end_station_latitude)
    df.dropna(subset=[key], inplace=True)
    return True

def is_bike(df, year):
    key = 'is_bike'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df[key] = 1
    return True

def start_time(df, year):
    key = 'start_time'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df.loc[:,key] = df['starttime'].apply(lambda x: time_to_val(x.time()))
    return True

def stop_time(df, year):
    key = 'stop_time'
    if key in df.columns:
        return False
    print("Adding bike feature: " + key)
    df.loc[:,key] = df['stoptime'].apply(lambda x: time_to_val(x.time()))
    return True

def add_all_features(df, year):
    new_added = False
    new_added = trip_distance(df, year) or new_added
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

# feature_functions = {
#     "trip_distance": lambda df, year: zones.haversine(df['start_station_latitude'], df['start_station_longitude'], df['end_station_latitude'], df['end_station_longitude']),
#     "day": lambda df, year: df.loc[:,'starttime'].map(lambda date: int(date.strftime('%d'))),
#     "zone_from": lambda df, year: np.vectorize(zones.lookup_id)(df.start_station_longitude, df.start_station_latitude),
#     "zone_to": lambda df, year: np.vectorize(zones.lookup_id)(df.end_station_longitude, df.end_station_latitude),
#     "zone_from_to": lambda df, year: np.vectorize(zones.from_to)(df.start_station_longitude, df.start_station_latitude, df.end_station_longitude, df.end_station_latitude),
#     "is_bike": lambda df, year: 1,
#     "start_time": lambda df, year: df['starttime'].apply(lambda x: time_to_val(x.time())),
#     "stop_time": lambda df, year: df['stoptime'].apply(lambda x: time_to_val(x.time()))
# }

# def add_feature(key, df, year):
#     if key in df.columns:
#         return False
#     if key not in feature_functions:
#         print("Failed to add feature " + key + " because no such function for this feature exists")
#         return False
#     print("Adding bike feature: " + key)
#     df.loc[:, key] = feature_functions[key](df, year)
#     df.dropna(subset=[key], inplace=True)
#     return True


# def add_all_features(df, year):
#     new_added = False
#     for key in feature_functions:
#         new_added = add_feature(key, df, year) or new_added
#     return new_added
    