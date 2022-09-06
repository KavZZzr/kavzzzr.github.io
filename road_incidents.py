from textwrap import indent
import requests
from geojson import Point, Feature, FeatureCollection, dump
from datetime import datetime
import time

# Open Data Portal Authentication
headers = {'Accept': 'application/octet-stream', 'Authorization' : 'apikey MJU7tfU64yNSXxHKXr6aeu3p5cjqmQ6tB2Cd'}

# Tidy up LiveTraffic JSON - remove tags etc.
rep = {'<p>':'', '</p>':'', '<strong>':'', '</strong>':'', '\t':'', '&nbsp;':' ', '<br>':'', '<a>':'', '</a>':''}
def replace_all(text):
    for i, j in rep.items():
        text = text.replace(i, j)
    return text

# Get feature collection for GeoJSON
def get_feature_collection(response):
    data_json = response.json()["features"]
    feature_list = []
    for incident in data_json:
        coordinates = incident["geometry"]["coordinates"]

        properties = incident["properties"]
        if "encodedPolylines" in properties: del properties["encodedPolylines"]
        roads = properties.pop("roads")
        impactedLanes = roads[0].pop("impactedLanes")
        for key in roads[0].keys(): 
            properties[key] = roads[0][key]
        if len(impactedLanes):
            for key in impactedLanes[0].keys(): 
                properties[key] = impactedLanes[0][key]
        properties["publicTransport"] = replace_all(properties["publicTransport"])
        properties["created"] = datetime.fromtimestamp(properties["created"]/1000).strftime('%#d %B %Y %#I:%M%p')
        properties["lastUpdated"] = datetime.fromtimestamp(properties["lastUpdated"]/1000).strftime('%#d %B %Y %#I:%M%p')
        if properties["mainCategory"] == 'Special event':
            properties["start"] = datetime.fromtimestamp(properties["start"]/1000).strftime('%#d %B %Y %#I:%M%p')
            properties["end"] = datetime.fromtimestamp(properties["end"]/1000).strftime('%#d %B %Y %#I:%M%p')
        properties["diversions"] = replace_all(properties["diversions"])
        properties["adviceB"] = replace_all(properties["adviceB"])
        properties["adviceA"] = replace_all(properties["adviceA"])
        properties["otherAdvice"] = replace_all(properties["otherAdvice"])

        point = Point((float(coordinates[0]),float(coordinates[1])))
        feature = (Feature(properties=properties, geometry=point))
        feature_list.append(feature)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection

# Separate function for all-feed-web.json

ignore_list = ['restAreas', 'hvcs', 'liveCams']

def get_other_incidents(response):
    data_json = response.json()
    feature_list = []
    for event in data_json:
        if event["eventType"] not in ignore_list:
            coordinates = event["geometry"]["coordinates"]

            properties = event["properties"]
            properties["apiSource"] = event["apiSource"]
            properties["eventType"] = event["eventType"]

            if event["apiSource"] == 'vicRoadInfo':
                if isinstance(properties["created"],int) : properties["created"] = datetime.fromtimestamp(properties["created"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if isinstance(properties["lastUpdated"],int) : properties["lastUpdated"] = datetime.fromtimestamp(properties["lastUpdated"]/1000).strftime('%#d %B %Y %#I:%M%p')
                roads = properties.pop("roads")
                for key in roads[0].keys(): properties[key] = roads[0][key]

            elif event["apiSource"] == 'qldRoad':
                if isinstance(properties["start"],int) : properties["start"] = datetime.fromtimestamp(properties["start"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if isinstance(properties["lastUpdated"],int) : properties["lastUpdated"] = datetime.fromtimestamp(properties["lastUpdated"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if properties["created"] != None and isinstance(properties["created"],int) : properties["created"] = datetime.fromtimestamp(properties["created"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if properties["end"] != None and isinstance(properties["end"],int) : properties["end"] = datetime.fromtimestamp(properties["end"]/1000).strftime('%#d %B %Y %#I:%M%p')
                roads = properties.pop("roads")
                impactedLanes = roads[0].pop("impactedLanes")
                for key in roads[0].keys(): properties[key] = roads[0][key]
                for key in impactedLanes.keys(): properties[key] = impactedLanes[key]

            elif event["apiSource"] == 'actRoadInfo':
                if isinstance(properties["start"],int) : properties["start"] = datetime.fromtimestamp(properties["start"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if isinstance(properties["end"],int) : properties["end"] = datetime.fromtimestamp(properties["end"]/1000).strftime('%#d %B %Y %#I:%M%p')
                roads = properties.pop("roads")
                for key in roads[0].keys(): properties[key] = roads[0][key]

            elif event["apiSource"] == 'saRoadInfo':
                if properties["start"] != None and isinstance(properties["start"],int) : properties["start"] = datetime.fromtimestamp(properties["start"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if properties["lastUpdated"] != None and isinstance(properties["lastUpdated"],int) : properties["lastUpdated"] = datetime.fromtimestamp(properties["lastUpdated"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if properties["created"] != None and isinstance(properties["created"],int) : properties["created"] = datetime.fromtimestamp(properties["created"]/1000).strftime('%#d %B %Y %#I:%M%p')
                if properties["end"] != None and isinstance(properties["end"],int) : properties["end"] = datetime.fromtimestamp(properties["end"]/1000).strftime('%#d %B %Y %#I:%M%p')
        

            point = Point((float(coordinates[0]),float(coordinates[1])))
            feature = (Feature(properties=properties, geometry=point))
            feature_list.append(feature)

    feature_collection = FeatureCollection(feature_list)
    return feature_collection
        

if __name__ == "__main__":

    while True:
        
        alpine_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/alpine/open'
        alpine_response = requests.get(alpine_link, headers=headers)
        if len(alpine_response.text)>0:
            alpine = get_feature_collection(alpine_response)
            with open('alpine.geojson', 'w') as f:
                dump(alpine, f, indent=4)
        
        fire_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/fire/open'
        fire_response = requests.get(fire_link, headers=headers)
        if len(fire_response.text)>0:
            fire = get_feature_collection(fire_response)
            with open('fire.geojson', 'w') as f:
                dump(fire, f, indent=4)

        flood_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/flood/open'
        flood_response = requests.get(flood_link, headers=headers)
        if len(flood_response.text)>0:
            flood = get_feature_collection(flood_response)
            with open('flood.geojson', 'w') as f:
                dump(flood, f, indent=4)

        incident_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/incident/open'
        incident_response = requests.get(incident_link, headers=headers)
        if len(incident_response.text)>0:
            incident = get_feature_collection(incident_response)
            with open('incident.geojson', 'w') as f:
                dump(incident, f, indent=4)

        majorevent_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/majorevent/open'
        majorevent_response = requests.get(majorevent_link, headers=headers)
        if len(majorevent_response.text)>0:
            majorevent = get_feature_collection(majorevent_response)
            with open('majorevent.geojson', 'w') as f:
                dump(majorevent, f, indent=4)

        roadwork_link = 'https://api.transport.nsw.gov.au/v1/live/hazards/roadwork/open'
        roadwork_response = requests.get(roadwork_link, headers=headers)
        if len(roadwork_response.text)>0:
            roadwork = get_feature_collection(roadwork_response)
            with open('roadwork.geojson', 'w') as f:
                dump(roadwork, f, indent=4)

        data_feeds_link = "https://www.livetraffic.com/datajson/all-feeds-web.json"
        data_feeds_response = requests.get(data_feeds_link)
        if len(data_feeds_response.text)>0:
            data_feeds = get_other_incidents(data_feeds_response)
            with open('all_feeds_web.geojson', 'w') as f:
                dump(data_feeds, f, indent=4)


        time_wait = 60
        print(f'Auto-refresh in {time_wait} seconds...')
        time.sleep(time_wait)
    