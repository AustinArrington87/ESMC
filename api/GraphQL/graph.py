import requests
import json

# Get Project abbreviations 
url = "https://gql.esmcportal.org/api/rest/project_names"
# add API credentials
header = {'x-hasura-admin-secret': 'EnterAPIKey'}
# call API
r = requests.get(url, headers=header)
print(r.json())

# get field data for GMP project 
url2 = "https://gql.esmcportal.org/api/rest/fields"
payload = {'abbr': 'GMP'}
r = requests.get(url2, headers=header, params=payload)
print(r.json())
