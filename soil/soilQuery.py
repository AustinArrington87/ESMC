import csv 
from datetime import date

today = date.today()

# script to get lat lons using the Core ID as reference

csv_file = "KS_GM.csv"

coreIDs = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        coreIDs.append(
            (row.get('CoreID'), row.get('ESRIGNSS_LATITUDE'), row.get('ESRIGNSS_LONGITUDE'))
        )
                                                                  
        
print(coreIDs)

csv_file2 = "GM_SoilData.csv"
gm_soil_data = []

with open(csv_file2, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gm_soil_data.append(
            (row.get('producer_id'), row.get('field_id'), row.get('year'), row.get('Core #'), row.get('SHAC #'), row.get('Depth (cm)'), row.get('soc'), row.get('bd'))
        )
        
print(gm_soil_data)

# headers in new CSV 
header = ['field_id', 'year', 'core_id', 'lat', 'lon', 'shac_id', 'depth', 'soc', 'bd']

with open('output_'+str(today)+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(header)
    
    for core in coreIDs:
        for data in gm_soil_data:
            if core[0] == data[3]:
                field_id = data[1]
                year = data[2]
                core_id = core[0]
                lat = core[1]
                lon = core[2]
                shac_id = data[4]
                depth = data[5]
                soc = data[6]
                bd = data[7]
                
                updated_data = [field_id, year, core_id, lat, lon, shac_id, depth, soc, bd]
                
                writer.writerow(updated_data)

print("DATA EXPORT COMPLETE")
                

                
                
                