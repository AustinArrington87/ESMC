import requests
from requests.auth import HTTPBasicAuth
import json


# load JSON file 
loadData = open("/Users/austinarrington/Desktop/PyScripts/API/data.json")
dicData = json.load(loadData)
print(dicData)

# make post request to DNDC 
url = "https://api.beta.rgrw.net/dndc-scenarios-service/api/submit"
# add API credentials
header = {'x-api-key': 'EnterAPIKey'}
# call API
r = requests.post(url, headers=header, json = dicData)
print(r.text)








