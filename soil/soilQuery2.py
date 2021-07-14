import csv 
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ESMC")

csv_file = "IL_Corn.csv"
coreIDs = []
ZIPs = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        coreIDs.append(
            (row.get('Project'), row.get('Lat'), row.get('Lon'))
        )
                                                                  
        
print(coreIDs)
print(len(coreIDs))
for core in coreIDs:
    if core is not None:
        locationString = core[1]+", "+core[2]
        try:
            location = geolocator.reverse(locationString)
            ZIP = location.raw['address']['postcode']
            ZIPs.append(ZIP)
            print("Core # "+str(coreIDs.index(core))+" Reverse Geocoding in Process...")
        except:
            pass
            ZIPs.append(ZIP)
    
print("Reverse Geocoding Complete!")
finalZIPs = []
[finalZIPs.append(x) for x in ZIPs if x not in finalZIPs]
print("ZIP Codes: ")
print(finalZIPs)

