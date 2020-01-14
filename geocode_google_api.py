
import pandas as pd 
import csv
import requests
import time
import json

df_locations = pd.read_csv('ENTER CSV OF ADDRESS HERE')

# function that accepts an address string, sends it to the Google API, and returns the lat-long API result
def geocode(address):
    time.sleep(1) #pause for some duration before each request, to not hammer their server
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=ENTER_API_KEY_HERE' #api url with placeholders
    request = url.format(address) #fill in the placeholder with a variable
    response = requests.get(request) #send the request to the server and get the response
    data = response.json() #convert the response json string into a dict
    
    if len(data['results']) > 0: #if google was able to geolocate our address, extract lat-long from result
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return '{},{}'.format(latitude, longitude) #return lat-long as a string in the format google likes

df_locations['latlng'] = df_locations['Address'].map(geocode)
df_locations['Latitude'] = df_locations['latlng'].map(lambda x: x.split(',')[0])
df_locations['Longitude'] = df_locations['latlng'].map(lambda x: x.split(',')[1])

#CREATES A GEOJSON FILE
def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}               # create a new python dict to contain our geojson data, using geojson format
    for _, row in df.iterrows():                                        # loop through each row in the dataframe and convert each row to geojson format
        feature = {'type':'Feature',
                'properties': {},
                'geometry':{'type':'Point',
                            'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon], row[lat]]       # fill in the coordinates
        for prop in properties:                                         # for each column, get the value and add it as a new feature property
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)                             # add this feature (aka, converted dataframe row) to the list of features inside our dict
    return geojson

cols = ['ENTER PANDA COLUMN NAMES HERE']  # select which columns to add to properties in geojson
geojson = df_to_geojson(df_locations, properties=cols)

# EXPORTS TO GEOJSON FILE
with open('ENTER NAME OF GEOJSON FILE HERE', 'w') as outfile:
    json.dump(geojson, outfile, indent=2)

print('Geojson file created succesfully.')

