import numpy as np
import xarray as xr

# info   https://gis.stackexchange.com/questions/299787/finding-pixel-location-in-raster-using-coordinates
# http://xarray.pydata.org/en/stable/generated/xarray.DataArray.values.html

# import file path for raster image 
filename = 'ICG-Field-3.tif'
filepath = '/Users/austinarrington/ESMC/data/rasters/'+str(filename)


latlons = [(-88.0293420670401, 39.9299906695464), (-88.03086459, 39.93006724), (-88.03203607, 39.93014691)]

for latlon in latlons:
    # iterate through array of locations 
    lon, lat = latlon[0], latlon[1]
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



