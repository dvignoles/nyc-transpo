def trip_duration(df):
    key = 'tripduration'
    if key in df.columns:
        return
    print("Adding feature" + key)
    df[key] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds()

def add_all_features(df):
    trip_duration(df)
