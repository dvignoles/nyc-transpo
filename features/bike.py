from features.common.zones import haversine

def trip_distance(df):
    key = 'trip_distance'
    if key in df.columns:
        return
    print("Adding feature " + key)
    df[key] = haversine(
    df['start_station_latitude'], 
    df['start_station_longitude'],
    df['end_station_latitude'], 
    df['end_station_longitude'])

def add_all_features(df):
    trip_distance(df)
