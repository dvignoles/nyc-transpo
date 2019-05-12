import numpy as np
import features.common.zones as zones

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

def add_all_features(df, year):
    new_added = False
    new_added = trip_duration(df, year) or new_added
    new_added = day(df, year) or new_added
    new_added = zone_from(df, year) or new_added
    new_added = zone_to(df, year) or new_added
    new_added = zone_from_to(df, year) or new_added
    return new_added
