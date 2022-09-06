from bs4 import BeautifulSoup
import requests
from geojson import Point, Feature, FeatureCollection, dump
import time


## NSW Incidents

def get_features_NSW(link):
    link_text = requests.get(link).text
    soup = BeautifulSoup(link_text, features='xml')
    feature_list =[]
    attribution = '© State of New South Wales (NSW Rural Fire Service). For current information go to www.rfs.nsw.gov.au.'
    disclaimer = "Disclaimer: While care is taken to ensure accuracy, the NSW Rural Fire Service cannot guarantee that information contained in RSS feeds is correct and recommends that users exercise their own skill and care with respect to its use."
    cap_data = soup.find_all('contentObject')
    for cap in cap_data:
        coordinates = cap.circle.text.split(' ')[0]
        lon = float(coordinates.split(',')[1])
        lat = float(coordinates.split(',')[0])
        point = Point((lon,lat))

        parameters = cap.find_all('parameter')
        para_list =[]
        for par in parameters:
            para_list.append(par.find('value').text)

        features = (Feature(properties = {
            'Incident Name' : cap.contentDescription.text.split(' ', 2)[2],
            'Published Time' : cap.sent.text,
            'Category' : cap.category.text,
            'Event' : cap.event.text,
            'Response Type': cap.responseType.text,
            'Urgency' : cap.urgency.text,
            'Severity' : cap.severity.text,
            'Certainty' : cap.certainty.text,
            'Effective' : cap.effective.text,
            'Expires' : cap.expires.text,
            'Source' : cap.senderName.text,
            'Alert Level' : cap.description.text.split('ALERT LEVEL: ')[1].split('<b')[0],
            'Location' : cap.areaDesc.text,
            'Council Area' : cap.description.text.split('COUNCIL AREA: ')[1].split('<b')[0],
            'Status' : cap.description.text.split('STATUS: ')[1].split('<b')[0],
            'Incident Type' : cap.description.text.split('TYPE: ')[1].split('<b')[0],
            'Incident Full Type' : para_list[12],
            'Fire' : cap.description.text.split('FIRE: ')[1].split('<b')[0],
            'Size (ha)' : float(cap.description.text.split('SIZE: ')[1].split(' ha')[0]),
            'Responsible Agency' : cap.description.text.split('RESPONSIBLE AGENCY: ')[1].split('<b')[0],
            'Last Updated' : cap.description.text.split('UPDATED: ')[1].split('<a')[0],
            'Instructions' : cap.instruction.text,
            'Fuel Type' : para_list[0],
            'Fire Danger Class' : para_list[2],
            'Fireground' : para_list[4],
            'Allocated Resources' : para_list[5],
            'Evacuation' : para_list[10],
            'Attribution' : attribution,
            'Disclaimer': disclaimer
        }, geometry=point))
        feature_list.append(features)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## WA Incidents

def get_features_WA_incidents(link):
    link_text = requests.get(link).text
    soup = BeautifulSoup(link_text, features='xml')
    feature_list =[]
    attribution = '© Government of Western Australia (Department of Fire and Emergency Services). For current information go to www.emergency.wa.gov.au.'
    items = soup.find_all('item')
    for item in items:
        lon = float(item.find('geo:long').text)
        lat = float(item.find('geo:lat').text)
        point = Point((lon,lat))

        features = (Feature(properties = {
            'Title' : item.title.text,
            'Link' : item.link.text,
            'Event' : item.description.text.split(' <')[0],
            'Region': item.description.text.split('<region>')[1].split('<')[0],
            'Incident Number': item.description.text.split('<incidentNumber>')[1].split('<')[0],
            'Published Time': item.pubDate.text,
            'Attribution': attribution
         }, geometry=point))
        feature_list.append(features)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection

def get_features_WA_warnings(link):
    link_text = requests.get(link).text
    soup = BeautifulSoup(link_text, features='xml')
    feature_list =[]
    attribution = '© Government of Western Australia (Department of Fire and Emergency Services). For current information go to www.emergency.wa.gov.au.'
    cap_data = soup.find_all('edxlde:contentObject')
    for cap in cap_data:
        coordinates = cap.find('cap:circle').text.split(' ')[0]
        lon = float(coordinates.split(',')[1])
        lat = float(coordinates.split(',')[0])
        point = Point((lon,lat))

        parameters = cap.find_all('cap:parameter')
        para_list =[]
        for par in parameters:
            para_list.append(par.find('cap:value').text)
            
        features = (Feature(properties = {
            'Incident Name' : cap.find('edxlde:contentDescription').text,
            'Status': cap.find('cap:status').text,
            'Message Type' : cap.find('cap:msgType').text,
            'Published Time' : cap.find('cap:sent').text,
            'Category' : cap.find('cap:category').text,
            'Event' : cap.find('cap:event').text,
            'Incident' : cap.find('cap:incidents').text,
            'Urgency' : cap.find('cap:urgency').text,
            'Severity' : cap.find('cap:severity').text,
            'Certainty' : cap.find('cap:certainty').text,
            'Source' : cap.find('cap:senderName').text,
            'Headline' : cap.find('cap:headline').text,
            'Location' : cap.find('cap:areaDesc').text,
            'Contact' : cap.find('cap:contact').text,
            'Alert Agency' : para_list[0],
            'Alert Note' : para_list[1],
            'Alert Details' : para_list[2],
            'Instructions' : cap.find('cap:instruction').text.replace('&nbsp;', ' '),
            'Attribution' : attribution
        }, geometry=point))
        feature_list.append(features)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection



## QLD Incidents

def get_features_QLD(link):
    response = requests.get(link)
    incidents = response.json()['features']
    feature_list=[]
    attribution = '© State of Queensland (Queensland Fire and Emergency Services). For current information go to www.qfes.qld.gov.au.'
    for incident in incidents:
        lon = float(incident['properties']['Longitude'])
        lat = float(incident['properties']['Latitude'])
        point = Point((lon,lat))
        
        properties = incident['properties']
        properties['Attribution'] = attribution
        features = (Feature(properties = properties, geometry=point)) 
        feature_list.append(features)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## VIC Incidents

def get_features_VIC(link):
    response = requests.get(link)
    incidents = response.json()['results']
    feature_list =[]
    attribution = '© CFA (Country Fire Authority). For current information go to www.emergency.vic.gov.au.'
    for incident in incidents:
        lon = float(incident['longitude'])
        lat = float(incident['latitude'])
        point = Point((lon,lat))
        
        incident['Attribution'] = attribution

        features = (Feature(properties = incident, geometry=point)) 
        feature_list.append(features)   
      
    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## SA Incidents

def get_features_SA(link):
    response = requests.get(link)
    incidents = response.json()
    feature_list =[]
    attribution = '© The Government of South Australia. For current information go to www.cfs.sa.gov.au.'
    for incident in incidents:
        lon = float(incident['Location'].split(',')[1])
        lat = float(incident['Location'].split(',')[0])
        point = Point((lon,lat))

        incident['Attribution'] = attribution

        features = (Feature(properties = incident, geometry=point)) 
        feature_list.append(features)
    
    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## TAS Incidents

def get_features_TAS(link):
    link_text = requests.get(link).text
    soup = BeautifulSoup(link_text, features='xml')
    feature_list =[]
    attribution = '© TFS (Tasmania Fire Service). For current information go to www.fire.tas.gov.au.'
    disclaimer = "Disclaimer: This information is extracted from the Tasmania Fire Service's Fire Incident Response Management (FIRM) system. This information is not necessarily 'real time' information, but is provided as a general indication of current activity. During outages of the TFS Website members of the public should refer to their ABC Local Radio for bushfire information and updates."
    items = soup.find_all('item')
    for item in items:
        lon = float(item.find('georss:point').text.split(' ')[1])
        lat = float(item.find('georss:point').text.split(' ')[0])
        point = Point((lon,lat))

        features = (Feature(properties = {
            'Title' : item.title.text,
            'Link' : item.link.text,
            'Category' : item.category.text,
            'Published Time' : item.pubDate.text,
            'Alert Level' : item.description.text.split('ALERT LEVEL: ')[1].split('<b')[0],
            'Region' : item.description.text.split('Region: ')[1].split('<b')[0],
            'Location' : item.description.text.split('LOCATION: ')[1].split('<b')[0],
            'Status' : item.description.text.split('STATUS: ')[1].split('<b')[0],
            'Type' : item.description.text.split('TYPE: ')[1].split('<b')[0],
            'Size' : item.description.text.split('SIZE: ')[1].split('<b')[0],
            'Number Of Vehicles' : item.description.text.split('Number of Vehicles: ')[1].split('<b')[0],
            'Responsible Agency' : item.description.text.split('RESPONSIBLE AGENCY: ')[1].split('<b')[0],
            'Last Updated' : item.description.text.split('UPDATED: ')[1].split('<b')[0],
            'Attribution' : attribution,
            'Disclaimer' : disclaimer
           }, geometry=point))   
        feature_list.append(features)
    
    feature_collection = FeatureCollection(feature_list)

    return feature_collection

## ACT Incidents

def get_features_ACT(link):
    link_text = requests.get(link).text
    soup = BeautifulSoup(link_text, features='xml')
    feature_list =[]
    attribution = '© ACT Emergency Services Agency. For current information go to www.esa.act.gov.au.'
    cap_data = soup.find_all('contentObject')
    for cap in cap_data:
        coordinates = cap.circle.text.split(' ')[0]
        lon = float(coordinates.split(',')[1])
        lat = float(coordinates.split(',')[0])
        point = Point((lon,lat))

        parameters = cap.find_all('parameter')
        para_list =[]
        for par in parameters:
            para_list.append(par.find('value').text)

        features = (Feature(properties = {
            'Incident Name' : cap.headline.text,
            'Published Time' : cap.sent.text,
            'Message Type' : cap.msgType.text,
            'Scope' : cap.scope.text,
            'Category' : cap.category.text,
            'Event' : cap.event.text,
            'Response Type': cap.responseType.text,
            'Urgency' : cap.urgency.text,
            'Severity' : cap.severity.text,
            'Certainty' : cap.certainty.text,
            'Effective' : cap.effective.text,
            'Expires' : cap.expires.text,
            'Source' : cap.senderName.text,
            'Location' : cap.description.text.split('Location: ')[1].splitlines()[0],
            'Status' : para_list[1],
            'Suburb' : cap.description.text.split('Suburb: ')[1].splitlines()[0],
            'Incident Type' : para_list[7],
            'Incident Full Type' : para_list[8],
            'Agency' : cap.description.text.split('Agency: ')[1].splitlines()[0],
            'Incident Number' : cap.description.text.split('Incident Number: ')[1].splitlines()[0],
            'Last Updated' : cap.description.text.split('Updated: ')[1].splitlines()[0],
            'Time of Call' : cap.description.text.split('Time of Call: ')[1].splitlines()[0],
            'Fireground' : para_list[2],
            'Control Authority' : para_list[3],
            'Alert Level' : para_list[4],
            'Council Area' : para_list[5],
            'Fire' : para_list[10],
            'Attribution' : attribution
        }, geometry=point))
        feature_list.append(features)

    feature_collection = FeatureCollection(feature_list)

    return feature_collection


if __name__ == "__main__":

    while True:

        ## Create GeoJSON NSW
        NSW_rss_link = 'https://www.rfs.nsw.gov.au/feeds/majorIncidentsCAP.xml'
        NSW_features = get_features_NSW(NSW_rss_link)
        with open('NSW_fire_emergency.geojson', 'w') as f:
            dump(NSW_features, f, indent=4)
        
        ## Create GeoJSON WA incidents
        WA_incidents_rss_link = 'https://www.emergency.wa.gov.au/data/incident_FCAD.rss'
        WA_incidents_features = get_features_WA_incidents(WA_incidents_rss_link)
        with open('WA_fire_emergency_incidents.geojson', 'w') as f:
            dump(WA_incidents_features, f, indent=4)
        
        ## Create GeoJSON WA warnings
        WA_warnings_rss_link =  'https://www.emergency.wa.gov.au/data/message_DFESCap.xml'
        WA_warnings_features = get_features_WA_warnings(WA_warnings_rss_link)
        with open('WA_fire_emergency_warnings.geojson', 'w') as f:
            dump(WA_warnings_features, f, indent=4)

        ## Create GeoJSON QLD
        QLD_rss_link = 'https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.json'
        QLD_features = get_features_QLD(QLD_rss_link)
        with open('QLD_fire_emergency.geojson', 'w') as f:
            dump(QLD_features, f, indent=4)

        ## Create GeoJSON VIC
        VIC_rss_link = 'https://data.emergency.vic.gov.au/Show?pageId=getIncidentJSON'
        VIC_features = get_features_VIC(VIC_rss_link)
        with open('VIC_fire_emergency.geojson', 'w') as f:
            dump(VIC_features, f, indent=4)

        ## Create GeoJSON SA
        SA_rss_link = 'https://data.eso.sa.gov.au/prod/cfs/criimson/cfs_current_incidents.json'
        SA_features = get_features_SA(SA_rss_link)
        with open('SA_fire_emergency.geojson', 'w') as f:
            dump(SA_features, f, indent=4)

        ## Create GeoJSON TAS
        TAS_rss_link = 'https://www.fire.tas.gov.au/Show?pageId=colBushfireSummariesRss'
        TAS_features = get_features_TAS(TAS_rss_link)
        with open('TAS_fire_emergency.geojson', 'w') as f:
            dump(TAS_features, f, indent=4)

        ## Create GeoJSON ACT
        ACT_rss_link = 'https://data.esa.act.gov.au/feeds/esa-cap-incidents.xml'
        ACT_features = get_features_ACT(ACT_rss_link)
        with open('ACT_fire_emergency.geojson', 'w') as f:
            dump(ACT_features, f, indent=4)

        time_wait = 60
        print(f'Auto-refresh in {time_wait} seconds...')
        time.sleep(time_wait)

