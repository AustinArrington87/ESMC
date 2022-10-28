import csv 
from datetime import date

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

csv_file2 = "GM_SoilData_102122.csv"
gm_soil_data = []

with open(csv_file2, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gm_soil_data.append(
            (row.get('Core #'), row.get('Depth (cm)'), row.get('SHAC #'), row.get('Bulk Density (g/cm3)'), 
                row.get('% Total Organic C'), row.get('P (ppm) soil '), row.get('pH water'), row.get('pH salt'),
                row.get('% Clay       < .002 mm'), row.get('% Silt               .002 - .050 mm'),
                row.get('% Sand               .050 - 2.00 mm'), row.get('Texture'))
        )
        
print(gm_soil_data)

# headers in new CSV 
header = ['core_id', 'lat', 'lon', 'depth', 'shac', 'bd', 'soc', 'p', 'ph_salt', 'ph_water', 'clay', 'silt', 'sand', 'texture']

with open('merged_'+csv_file2, 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(header)
    
    for core in coreIDs:
        for data in gm_soil_data:
            if core[0] == data[0]:
                core_id = core[0]
                lat = core[1]
                lon = core[2]
                depth = data[1]
                shac_id = data[2]
                bd = data[3]
                soc = data[4]
                p = data[5]
                ph_salt = data[6]
                ph_water = data[7]
                clay = data[8]
                silt = data[9]
                sand = data[10]
                texture = data[11]
                
                updated_data = [core_id, lat, lon, depth, shac_id, bd, soc, p, ph_salt, ph_water, clay, silt, sand, texture]
                
                writer.writerow(updated_data)

print("DATA EXPORT COMPLETE")
                
