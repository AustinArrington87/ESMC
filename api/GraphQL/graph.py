import requests
import json

# make post request to Project Names GraphQL Endpoint
url = "https://gql.esmcportal.org/api/rest/project_names"
# add API credentials
header = {'x-hasura-admin-secret': 'EnterSecret'}
# call API
r = requests.get(url, headers=header)
print(r.text)

