import numpy as np
import xarray as xr
import csv

# info   https://gis.stackexchange.com/questions/299787/finding-pixel-location-in-raster-using-coordinates
# http://xarray.pydata.org/en/stable/generated/xarray.DataArray.values.html

# read in lat lons from soil_sample CSV
sampledata = []
csv_file = 'ICG-Field-33.csv'

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sampledata.append(
            (row.get('year'), row.get('point'), row.get('start_depth'), row.get('end_depth'), row.get('lon'), row.get('lat'), row.get('dry_weight'), row.get('soc'), row.get('field'))
        )

# import file path for raster image 
filename = 'ICG-Field-33.tif'
filepath = '/Users/austinarrington/ESMC/data/rasters/'+str(filename)

# headers for new CSV 
header = ['field', 'year', 'point', 'start_depth', 'end_depth', 'lon', 'lat', 'dry_weight', 'soc', 'bd']

with open('output.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    # write header
    writer.writerow(header)
    
    for data in sampledata:
        year = data[0]
        point = data[1]
        start_depth = data[2]
        end_depth = data[3]
        # iterate through array of locations
        lon, lat = data[4], data[5]
        dry_weight = data[6]
        soc = data[7]
        field = data[8]
        # read in file 
        xarr = xr.open_rasterio(filepath)
        # slice one of the bands
        img = xarr[0, :, :]
        #Use the .sel() method to retrieve the value of the nearest cell close to your POI
        val = img.sel(x=lon, y=lat, method="nearest")
        # convert arrays data to numpy data array
        bulk_density = val.values
        # convert numpy data array to float and round to 4 decimals
        bd = round(float(bulk_density),4)
        print("Bulk Density (g/cm3): ", bd, " | ", lat, ",", lon)
        
        data = [field, year, point, start_depth, end_depth, lon, lat, dry_weight, soc, bd]
        writer.writerow(data)