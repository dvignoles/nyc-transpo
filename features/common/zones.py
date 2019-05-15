import numpy as np
import preprocessing.constants as constants

ZONES = constants.ZONES
ZONES_DIC = constants.ZONES_DIC

class Zone:
    def __init__(self,location_id,name,borough,area,bbox):
            self.location_id = location_id
            self.name = name
            self.borough = borough
            self.area = area
            self.bbox = bbox
    
    def __repr__(self):
        return str((self.location_id,self.name,self.borough,self.area,self.bbox))
    
    def __str__(self):
        return(self.name + ' : ' + str(self.bbox))

import shapefile #pip install pyshp
with shapefile.Reader("./taxi_zones/geo_export_a619f821-072d-486f-8172-0c1be3f7e97d") as shp:
    shapes = shp.shapes()
    
    fields = shp.fields
    
    records = shp.records()

#Populate ZONES/ZONES_DIC
for i in range(0,len(shapes)):
    z = Zone(records[i].location_i,records[i].zone,records[i].borough,records[i].shape_area,shapes[i].bbox)
    ZONES.append(z)
    ZONES_DIC[str(z.location_id)] = z

def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a)) * .62137
  

def lookup(lon,lat):
    '''Return Zone object if lon/lat return valid taxi zone'''
    for z in ZONES: #probably should not do this in a for loop
        
        w_lon = z.bbox[0]
        s_lat = z.bbox[1]
        e_lon = z.bbox[2]
        n_lat = z.bbox[3]
        
        if lat >= s_lat and lat <= n_lat:
            if lon >= w_lon and lon <= e_lon:
                return(z)
    return None

def lookup_id(lon,lat):
    '''Get the Taxi zone ID number from lon/lat'''
    z = lookup(lon,lat)
    
    if z:
        return z.location_id
    else:
        return np.nan

def from_to(from_lon,from_lat,to_lon,to_lat):
    '''Return string showing taxi to from ie: Tribecca to Central park'''
    z_from = lookup(from_lon,from_lat)
    z_to = lookup(to_lon,to_lat)
    try:
        return z_from.name + ' to ' + z_to.name
    except:
        return np.nan

def from_to_zid(from_id, to_id):
    try:
      return zones.ZONES_DIC[str(float(from_id))].name + ' to ' + zones.ZONES_DIC[str(float(to_id))].name
    except Exception as ex:
      return np.nan
