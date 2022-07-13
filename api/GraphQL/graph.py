import requests
import json

# make post request to Project Names GraphQL Endpoint
url = "https://gql.esmcportal.org/api/rest/project_names"
# add API credentials
header = {'x-hasura-admin-secret': 'D2FwLafuZdMQuDue7gv66xkD8xuSgW'}
# call API
r = requests.get(url, headers=header)
print(r.text)

