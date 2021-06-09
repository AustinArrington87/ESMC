import requests
import xmltodict
import json
import re
from pyproj import Proj
from pyproj import transform
import pycrs

# resources: https://pyproj4.github.io/pyproj/v1.9.6rel/pyproj-pysrc.html

# CropScape https://nassgeodata.gmu.edu/CropScape/devhelp/help.html

# https://gis.stackexchange.com/questions/307620/projection-conversion-with-python-pyproj-canada-albers-equal-area-to-wgs
#  EPSG code of Canada Equal Area as 102001 (see https://epsg.io/102001),

year = 2018

#Canada Albers Equal Area Conic: ESRI:102001 is not an EPSG SRID value but an ESRI SRID value not recognized by PyProj.
#So use the PROJ4 string of Canada Albers Equal Area Conic: ESRI:102001.
        
# convert lat lon coordinates to ESRI:102001 - not working yet
lat,lon = (-95.09215, 40.57527)
crs = pycrs.parse.from_esri_code(102001)
inproj = Proj(init='epsg:4326')
outproj = Proj( crs.to_proj4())
x,y = transform(inproj,outproj,lat,lon)
print(x)
print(y)

response = requests.get('https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLValue?year='+str(year)+'&x=1551565.363&y=1909363.537')

#response = requests.get('https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLValue?year=2017&x='+str(x)+'&y='+str(y))

# parse xml to json string 
response_dict = xmltodict.parse(response.text)
json_data = json.dumps(response_dict)
# convert string to response
res = json.loads(json_data)
print(res)
result = res["ns1:GetCDLValueResponse"]["Result"]
print(result)
# parse croptype from string using Regex
crop_result = re.search(r'category:(.*?)color', result).group(1)
# remove special characters 
crop_result = crop_result.replace(',', '')
crop_result = crop_result.replace('"', '')
print(crop_result)



