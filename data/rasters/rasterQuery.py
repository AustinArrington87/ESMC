import numpy as np
import xarray as xr

# info   https://gis.stackexchange.com/questions/299787/finding-pixel-location-in-raster-using-coordinates
# http://xarray.pydata.org/en/stable/generated/xarray.DataArray.values.html

# import file path for raster image 
filename = 'ICG-Field-3.tif'
filepath = '/Users/austinarrington/ESMC/data/rasters/'+str(filename)

# define location 
lon1, lat1 = (-88.0293420670401, 39.9299906695464)
# read in file 
xarr = xr.open_rasterio(filepath)
# Slice one of the bands
img = xarr[0, :, :]
#Use the .sel() method to retrieve the value of the nearest cell close to your POI
val = img.sel(x=lon1, y=lat1, method="nearest")
# convert arrays data to numpy data array
bulk_density = val.values
# convert numpy data array to float and round to 4 decimals 
bd = round(float(bulk_density),4)
print("Bulk Density (g/cm3): ", bd)

