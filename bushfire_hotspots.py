import requests
from geojson import Point, Feature, FeatureCollection, dump



def get_hotspots(link):
    response = requests.get(link)
    hotspots = response.json()['features']
    feature_list =[]
 
    for hotspot in hotspots:
        lon = float(hotspot['properties']['longitude'])
        lat = float(hotspot['properties']['latitude'])
        point = Point((lon,lat))

        feature = (Feature(properties = hotspot['properties'], geometry=point))
        feature_list.append(feature)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## GeoJSON
##### Note: Please attribute © Commonwealth of Australia (Geoscience Australia) 2021
link = 'https://hotspots.dea.ga.gov.au/data/recent-hotspots.json'

hotspots = get_hotspots(link)
with open('bushfire_hotspots.geojson', 'w') as f:
    dump(hotspots, f, indent=4)