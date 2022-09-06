import subprocess
import time

## requires tilesets-cli https://github.com/mapbox/tilesets-cli
## Assumes all GeoJSON files in same folder 

path_to_geojson = "\\PATH\\TO\\GEOJSON"
username = 'stevegrehan'
mapbox_token = 'sk.eyJ1Ijoic3RldmVncmVoYW4iLCJhIjoiY2w1OTB5cXRyMjR4ZjNrbjlobDljNDc5eCJ9.ycpQcf7LdFiKqsii02mPmw'
# mapbox_token = 'sk.eyJ1Ijoia2F2aW5kdS1yYW5hc2luZ2hlIiwiYSI6ImNsNWtkeGY2aTA2cjQzYnBiczZzaXNpY20ifQ.hoIfqKIEhoTPI2xEkZkSwQ'

sources = {'all-feeds-web-source': 'all_feeds_web.geojson',
            'alpine-source': 'alpine.geojson',
            'fire-source': 'fire.geojson',
            'flood-source': 'flood.geojson',
            'incident-source': 'incident.geojson',
            'majorevent-source': 'majorevent.geojson',
            'roadwork-source': 'roadwork.geojson',
            # 'act-source': 'ACT_fire_emergency.geojson',
            # 'nsw-source': 'NSW_fire_emergency.geojson',
            # 'qld-source': 'QLD_fire_emergency.geojson',
            # 'vic-source': 'VIC_fire_emergency.geojson',
            # 'sa-source': 'SA_fire_emergency.geojson',
            # 'wa-source': 'WA_fire_emergency.geojson',
            # 'tas-source': 'TAS_fire_emergency.geojson'
            }

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


if __name__ == '__main__':

    run(f"cd {path_to_geojson}")
    while True:
        
        for key in sources.keys():
            success = run(f"tilesets upload-source {username} {key} {sources[key]} --replace --token {mapbox_token}")
            if success != 0:
                print("An error occured: %s", success.stderr)
            else:
                print(f"{key} updated successfully!")

        time_wait = 2*3600
        print(f'Next update in {time_wait/3600} hours...')
        time.sleep(time_wait)