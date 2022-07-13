import requests
import json

# load JSON file 
loadData = open("test.json", 'r')
dicData = json.loads(loadData.read())
print(dicData)

# make post request to DNDC 
url = "https://api.beta.rgrw.net/dndc-scenarios-service/api/submit"
# add API credentials
header = {'x-apikey': 'enter api key'}
# call API
r = requests.post(url, headers=header, json = dicData)
print(r.text)








