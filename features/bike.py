import numpy as np
import features.common.zones as zones


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


def add_all_features(df, year):
    new_added = False
    new_added = trip_distance(df, year) or new_added
    new_added = day(df, year) or new_added
    new_added = zone_from(df, year) or new_added
    new_added = zone_to(df, year) or new_added
    new_added = zone_from_to(df, year) or new_added
    return new_added
    