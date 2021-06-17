import numpy as np
import xarray as xr
import csv

# info   https://gis.stackexchange.com/questions/299787/finding-pixel-location-in-raster-using-coordinates
# http://xarray.pydata.org/en/stable/generated/xarray.DataArray.values.html

# read in lat lons from soil_sample CSV
sampledata = []
csv_file = 'IL_SoilData.csv'

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sampledata.append(
            (row.get('year'), row.get('lon'), row.get('lat'))
        )

# import file path for raster image 
filename = 'ICG-Field-3.tif'
filepath = '/Users/austinarrington/ESMC/data/rasters/'+str(filename)

# headers for new CSV 
header = ['year', 'lon', 'lat', 'bd']

with open('output.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    # write header
    writer.writerow(header)
    
    for data in sampledata:
        year = data[0]
        # iterate through array of locations
        lon, lat = data[1], data[2]
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
        
        data = [year, lon, lat, bd]
        writer.writerow(data)