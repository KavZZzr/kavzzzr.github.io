import os

mydir = 'C:/Users/61420/OneDrive - insitec.com.au/Documents/GitHub/WebScraping'
for f in os.listdir(mydir):
    if not f.endswith(".geojson"):
        continue
    os.remove(os.path.join(mydir, f))