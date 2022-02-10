import csv
import geocoder
import itertools
import reverse_geocoder as rg
import pprint
from collections import OrderedDict
import json

fields = []
field_edit = []
practices = []
practices_edit = []
crops = []

def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    #pprint.pprint(result)
    result = json.loads(json.dumps(result))
    return(result)

coordinates = (38.60088986, -85.66500328)
location = reverseGeocode(coordinates)
print(location[0])
# state 
print(location[0]['admin1'])
# county 
print(location[0]['admin2'])

projects = ['Benson Hill', 'Corteva', 'General Mills', 'Illinois Corn Growers', 'Missouri Partnership Pilot', 'TNC Minnesota']

# buckets for projects 
benson_hill = []
corteva = []
general_mills = []
il_corn = []
mo_partner = []
tnc_mn = []

csv_file = "practice_changes.csv"
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fields.append(
            (row.get('fieldid'))
        )
        
        try: 
            coordinates = (row.get('latitude'), row.get('longitude'))
            location = reverseGeocode(coordinates)
            state = location[0]['admin1']
            print(state)
            county = location[0]['admin2']
            print(county)
        except:
            state = None
            county = None
        
        practices.append(
            (row.get('projectname'), row.get('farmer__app_user__id'), row.get('status'), row.get('fieldid'), row.get('acres'), row.get('latitude'), row.get('longitude'), row.get('practicechange'), row.get('yield'), row.get('name'), row.get('commodity_other_name'), row.get('unit'), state, county)
        )

#print(practices)
print("Writing to CSV...")
###################################
###################################

# Now write to a new CSV 
headers = ['projectname', 'state', 'county', 'farmer__app_user__id', 'status', 'fieldid', 'acres', 'latitude', 'longitude', 'practicechange', 'crop', 'crop_other', 'yield', 'unit']

with open('output.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    # write header 
    writer.writerow(headers)
    for data in practices:
        project_name = data[0]
        state = data[12]
        county = data[13]
        farmer_id = data[1]
        status = data[2]
        field_id = data[3] 
        acres = data[4]
        lat = data[5]
        lon = data[6]
        practice_change = data[7]
        crop_type = data[9]
        crop_other = data[10]
        crop_yield = data[8]
        unit = data[11]
        
        data = [project_name, state, county, farmer_id, status, field_id, acres, lat, lon, practice_change, crop_type, crop_other, crop_yield, unit]
        
        writer.writerow(data)
        

    
#for practice in practices: 
#    result = geocoder.google(practice[7]+', '+practice[8], reverse=True)
#    print(result)

# now remove duplicate rows (there are duplicate fields because some have multiple harvest)
#new_k = []
#for elem in practices:
#    if elem not in new_k:
#        new_k.append(elem)
#practices = new_k
#print(len(practices))
#
## now bucket out practices by project 
#for practice in practices:
#    #print(practice)
#    
#    if practice[0] == 'Benson Hill':
#        benson_hill.append(practice)
#    if practice[0] == 'Corteva':
#        corteva.append(practice)
#    if practice[0] == 'General Mills':
#        general_mills.append(practice)
#    if practice[0] == 'Illinois Corn Growers':
#        il_corn.append(practice)
#    if practice[0] == 'Missouri Partnership Pilot':
#        mo_partner.append(practice)
#    if practice[0] == 'TNC Minnesota':
#        tnc_mn.append(practice)
#    
#    crops.append(practice[9])
#
#print("Benson Hill Fields: ", len(benson_hill))
#print("Corteva Fields: ", len(corteva))
#print("General Mills Fields: ", len(general_mills))
#print("Illinois Corn Growers Fields: ", len(il_corn))
#print("Missouri Partnership Fields: ", len(mo_partner))
#print("TNC Minnesota Fields: ", len(tnc_mn))
#
## remove duplicates from crop list 
#crop_edit = []
#for crop in crops:
#    if crop not in crop_edit:
#        crop_edit.append(crop)
#
#print(crop_edit)
# ['Soybeans', 'Corn', '[NULL]', 'Hay/Alfalfa', 'Wheat', 'Rye', 'Barley', 'Other', 'Corn Silage', 'Sorghum']
# now loop through each bucket 


