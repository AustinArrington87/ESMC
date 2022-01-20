import json

# Functions
# remove the nulls and sum up the yields per crop 
def removeNull(cropAcres):
    newList = []
    for val in cropAcres:
        if val != None:
            newList.append(val)
    return sum(newList)
# LOAD DATA 
file = open('Corteva_1.19.22_Final.json')
data = json.load(file)

enrollment_year = 2021
histmin1_year = enrollment_year-1
histmin2_year = enrollment_year-2
histmin3_year = enrollment_year-3

assets = []
projects = []
producers = []
prod_ids = []
fields = []
totalFields = []
practices = []
acres = []
crops = []
enrollment_crops = []
histmin1_crops = []
histmin2_crops = []
histmin3_crops = []
enrollment_cropType = []
histmin1_cropType = []
histmin2_cropType = []
histmin3_cropType = []
# crop acres 
other_acres = []
cotton_acres = []
barley_acres = []
corn_silage_acres = []
rye_acres = []
soybean_acres = []
corn_acres = []
wheat_acres = []

for ass in data:
    assets.append(ass["assets"])

for proj in data:
    projects.append(proj["project"])

for prod in data:
    producers.append(prod["producers"])

print("PROJECT: ", projects[0])
print("ASSETS: ")
for ass in assets:
    print(ass)
print("============PRODUCERS==================")
print("Number of Producers: ", len(producers[0]))
print("___________________________________")
for prod in producers[0]:
    print(prod["user_by_project_id"], "| Producer Agreement: ", prod["has_agreed_to_producer_agreement"])
    fields.append(prod['fields'])
    try:
        for field in fields:
            #print(field)
            for f in field:
                print(f['field_by_project_id'], "|", f['area']['value'], f['area']['unit'])
                #print(f['area']['value'], f['area']['unit'])
                acres.append(f['area']['value'])
                totalFields.append(f['field_by_project_id'])
                practices.append(f["field_practice_changes"])
                
                for j in f['history']:
                    
                    if j['year'] == enrollment_year:
                        for k in j['event_data']:
                            if k['event'] == 'Harvest':
                                enrollment_crops.append([k['crop'],k['yield']['value']])
                                enrollment_cropType.append(k['crop'])
                    if j['year'] == histmin1_year:
                        for k in j['event_data']:
                            if k['event'] == 'Harvest':
                                histmin1_crops.append([k['crop'],k['yield']['value']])
                                histmin1_cropType.append(k['crop'])
                    if j['year'] == histmin2_year:
                        for k in j['event_data']:
                            if k['event'] == 'Harvest':
                                histmin2_crops.append([k['crop'],k['yield']['value']])
                                histmin2_cropType.append(k['crop'])
                    if j['year'] == histmin3_year:
                        for k in j['event_data']:
                            if k['event'] == 'Harvest':
                                histmin3_crops.append([k['crop'],k['yield']['value']])
                                histmin3_cropType.append(k['crop'])
                    
                    
                    #print(j['event_data'])
                    for k in j['event_data']:
                        
                        if k['event'] == 'Harvest':
                            print(j['year'], "Harvest:", k['crop'], "|", k['yield']['value'], k['yield']['unit'])
                            crops.append(k['crop'])
                        
                
                for prac in practices:
                    for p in prac:
                        print("Practice Change:", p['name'])
                practices.clear()
                print("___________________________________")
    
        print("===================================")
        field.clear()
    except:
        pass

print("============TOTAL==FIELDS==================")
#print(totalFields)
print("Total Fields: ", len(totalFields))
print("Total Acres: ", round(sum(acres),2))

# these are the possible crops included in enrollment and historical years 
print(str(enrollment_year),"Crop Types:", set(enrollment_cropType))
print(str(histmin1_year),"Crop Types:", set(histmin1_cropType))
print(str(histmin2_year),"Crop Types:", set(histmin2_cropType))
print(str(histmin3_year),"Crop Types:", set(histmin3_cropType))

#print(enrollment_crops)

# now let's check total acres for our enrollment year crops harvest 
for crop in enrollment_crops:
    if crop[0] == 'Corn':
        corn_acres.append(crop[1])
    if crop[0] == 'Soybeans':
        soybean_acres.append(crop[1])
    if crop[0] == 'Corn Silage':
        corn_silage_acres.append(crop[1])
    if crop[0] == 'Wheat':
        wheat_acres.append(crop[1])
    if crop[0] == 'Rye':
        rye_acres.append(crop[1])
    if crop[0] == 'Barley':
        barley_acres.append(crop[1])

#print(corn_acres)
#print(soybean_acres)
#print(corn_silage_acres)
#print(wheat_acres)
#print(rye_acres)
#print(barley_acres)

# remove the nulls and sum up the yields per crop 
print(str(enrollment_year),"Total Corn Harvest:", removeNull(corn_acres), "bu/acre")
print(str(enrollment_year),"Total Soybean Harvest:", removeNull(soybean_acres), "bu/acre")
print(str(enrollment_year),"Total Corn Silage Harvest:", removeNull(corn_silage_acres), "tons/acre")
print(str(enrollment_year),"Total Wheat Harvest:", removeNull(wheat_acres), "bu/acre")


