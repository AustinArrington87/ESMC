# %%
# Upload payload to the Production Server
import json
import requests
import getOAuth
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def post(jsonFile,token):
    baseURL = os.getenv("OAUTH2_PROXY_OIDC_ISSUER_URL")
    print(baseURL)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    with open(jsonFile) as json_file:
        data = json.load(json_file)
    return requests.post(baseURL+'/api/intake/submit',json=data,headers=headers)

# %%
