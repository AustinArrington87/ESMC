import requests
import xmltodict
import json
import re
import pyproj

# resources: https://pyproj4.github.io/pyproj/v1.9.6rel/pyproj-pysrc.html
# CropScape https://nassgeodata.gmu.edu/CropScape/devhelp/help.html
# https://gis.stackexchange.com/questions/307620/projection-conversion-with-python-pyproj-canada-albers-equal-area-to-wgs
# Convert EPSG code of Canada Equal Area as 102001 (see https://epsg.io/102001) to lat lon EPSG:4326

def getCrop (year,lat,lon):
    inproj = pyproj.Proj(init='epsg:4326')
    outproj = pyproj.Proj('+proj=aea +lat_1=50 +lat_2=70 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs')
    lon, lat = (-71.15884110801677, 54.679405476637065)
    x,y = pyproj.transform(inproj,outproj,lon,lat)
    #print(x)
    #print(y)

    response = requests.get('https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLValue?year='+str(year)+'&x='+str(x)+'&y='+str(y))

    # parse xml to json string 
    response_dict = xmltodict.parse(response.text)
    json_data = json.dumps(response_dict)
    # convert string to response
    res = json.loads(json_data)
    #print(res)

    result = res["ns1:GetCDLValueResponse"]["Result"]
    #print(result)
     #parse croptype from string using Regex
    crop_result = re.search(r'category:(.*?)color', result).group(1)
     #remove special characters 
    crop_result = crop_result.replace(',', '')
    crop_result = crop_result.replace('"', '')
    return crop_result

# feed year, lat, lon into function 
years = [2019, 2018, 2017, 2016, 2015]
for year in years:
    crop = getCrop(year, 54.679405476637065, -71.15884110801677)
    print("Year: ", year, "|", crop)



