# %%
# Setup utilities for the MRV API

# Import libraries
import argparse
from distutils.command.config import config
from formatter import NullFormatter
from lib2to3.pgen2 import token
from os import environ
from os import path
from dotenv import dotenv_values
from keycloak import KeycloakOpenID
import json
import requests
import psycopg2
import time
from requests_toolbelt import MultipartEncoder
import os
import datetime

# Global configure dictionary
config = None
openid = None
tokenRefresh = None

    
# %%
def addField(producerId, fieldFile, year, isSingleField='true'):
    
    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    fileBasename = path.basename(fieldFile)
    
    payload = MultipartEncoder(
        fields = {
            'field':  (fileBasename,open(fieldFile,'rb'),'application/octet-stream'),
            'hasAcceptedWarning': 'false',
            'selectedEnrollmentYear': year,
            'isSingleField': isSingleField
        }
    )
    header['Content-Type'] = payload.content_type
    urlParams = {'guest': producerId}
    
    return requests.post(config['mrvUrl']+'/api/field/upload-boundaries/',headers=header,params=urlParams,data=payload)


# %%
def configure(environmentFile):
    
    global config
    
    if not path.exists(environmentFile):
        raise Exception(f"The specified environment settings file, {environmentFile}, does not exist.")
    
    configTmp = dotenv_values(environmentFile)
    requiredKeys = set(['keycloakUser','keycloakPassword','keycloakClientSecret','keycloakClientId','keycloakRealmName',
                        'keycloakAuthUrl','mrvUrl','dbHost','dbPort','dbUser','dbPassword','dndcApiKey','dndcUrl',
                        'graphqlUrl'])
    if not requiredKeys.issubset(configTmp.keys()):
        raise Exception(f'The environment file is missing one of more of the following required keys: {requiredKeys}')
    else:
        config = configTmp

    return config

#%%
def configIsValid():

    global config
    if not config:
        raise Exception('mrvApi.configure(environmentFile) must be run first.')
    else:
        return True    
    

# %%
def connectToDb():
    
    # Validate inputs
    global config
    assert(configIsValid())
    
    try:
        return psycopg2.connect(
            database="esmc_prod_v2",
            user=config['dbUser'],
            password=config['dbPassword'],
            host=config['dbHost'],
            port=config['dbPort'],
        )
    except:
        return False


# %%
def dndcExport(fieldId, year, reset_baselines=False):
    
    print('Export started')
    
    conn = connectToDb()
    if conn:
        curr = conn.cursor()
        curr.execute(f"select * from farm.get_model_dndc('{fieldId}'::uuid, '{year}'::smallint, '{reset_baselines}')")
        data = curr.fetchall()
        curr.close()
        conn.commit()
        conn.close()
        
        print('Export finished')
        return data
        
    else:
        conn.close()
        raise Exception('Unable to connect to the database')

# %%
def dndcGetProject(projectName, saveToFile=None):
    
    global config
    assert(configIsValid)
    
    dndcUrl = 'https://api.beta.rgrw.net/dndc-scenarios-service/api/field_level_scope_3'
    dndcHeader = {
        'x-apikey':config['dndcApiKey']
    }
    urlParams = {
        'project_name': projectName
    }
    
    rsp = requests.get(dndcUrl, headers=dndcHeader, params=urlParams)
    
    if saveToFile:
        with open(saveToFile,"w") as dndcFile:
            json.dump(json.loads(rsp.text),dndcFile,indent=4)
    
    return rsp

# %%
def dndcPayload(fieldId, year):
    
    export = dndcExport(fieldId, year)[0][0]
    
    if export['esmc_error']:
        return None
    else:
        return export['request_body']
    

# %%
def dndcRequest(projectName, payload):
    
    global config
    assert(configIsValid)
    
    dndcUrl = config['dndcUrl']
    dndcHeader = {
        'x-apikey':config['dndcApiKey']
    }
    urlParams = {
        'project_name':projectName
    }

    rsp = requests.post(dndcUrl, headers=dndcHeader, params=urlParams, json=payload)
    try:
        return (json.loads(rsp._content.decode()))
    except:
        return (rsp._content.decode())
    

# %%
def dndcRequestField(projectName, fieldId, year, exportData=None, reset_baselines=False):
    
    print(f"dndcRequestField: Project - {projectName}, Field Id - {fieldId}")
    
    if not exportData:
        exportData = dndcExport(fieldId, year, reset_baselines=reset_baselines)[0][0]
    
    header = refreshHeader()

    modelResults = {
        'projectName': projectName,
        'requestBody': exportData['request_body'],
        'fieldId': fieldId,
        'farmerProjectSeasonId':exportData['farmer_project_season__id'],
        'sessionName':exportData['session_name'],
        'esmcError':exportData['esmc_error']
    }

    if exportData['esmc_error']:
        modelResults['sessionId'] = None
        modelResults['response'] = None
        modelResults['modelStatusValue'] = 'NOT_SENT'
    else:
        dndcRsp = dndcRequest(projectName, exportData['request_body'])
        
        if 'data' in dndcRsp:
            modelResults['sessionId'] = dndcRsp['data']['id']
            modelResults['response'] = dndcRsp['data']
            modelResults['modelStatusValue'] = 'REQUEST_GENERATED'
        else:
            modelResults['sessionId'] = None
            modelResults['modelStatusValue'] = 'MODEL_ERROR'
            if 'detail' in dndcRsp:
                modelResults['response'] = dndcRsp['detail']
            else:
                modelResults['response'] = dndcRsp

    header['x-hasura-role'] = "esmc-admin"
    dataJson = json.dumps(modelResults)
    rsp = requests.post(config['graphqlUrl']+'/api/rest/saveModelDndc',headers=header,data=json.dumps(modelResults))
    print(f"dndcRequestField: model_status - {modelResults['modelStatusValue']}")


# %%
def dndcRequestProducer(projectName, producerId, year, reset_baselines=False):
    
    print(f"dndcRequestProducer: Project - {projectName}, Producer ID - {producerId}")
    
    summary = fieldSummary(producerId, year)
    
    if 'fields' in summary:
        for field in summary['fields']:
            dndcRequestField(projectName, field['id'], year, reset_baselines=reset_baselines)
            # time.sleep(1.05)
        
        
# %%
def dndcRequestProject(projectName, year, reset_baselines=False):
    
    print(f"dndcRequestProject: Project - {projectName}")
    
    projId = projectId(projectName)
    if projId == None:
        raise Exception("Invalid project name")
    
    producers = enrolledProducers(projId, year)
    
    dateTime = str(datetime.datetime.now())
    for producer in producers:
        print(f"dndcRequestProject: Producer - {producer['name']}")
        dndcRequestProducer(projectName+dateTime, producer['id'], year, reset_baselines=reset_baselines)
        
    
# %%
def enrolledProducers(projectId, year):

    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    urlParams = {
        'review': 'false',
        'selectedEnrollmentYear': year
    }
    payload = {
        'skip': '0',
        'take': '200000'
    }
    producers = json.loads(requests.post(config['mrvUrl']+'/api/project/'+projectId+'/enrolledProducers',headers=header,params=urlParams,json=payload).text)
    enrolled = []
    for producer in producers['data']:
        enrolled.append({'id':producer['id'], 'name':producer['name'], 'email':producer['email']})
    return enrolled
    
# %%
def eventsAllFields(producerId, year):

    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    data = {
        'type': 'summary',
        'selectedEnrollmentYear': year,
        'guest': producerId
    }
    
    return json.loads(requests.get(config['mrvUrl']+'/api/event-data',headers=header,params=data).text)


# %%
def events(fieldId, producerId, year):
    
    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    data = {
        'type': 'summary',
        'selectedEnrollmentYear': year,
        'guest': producerId,
        'fieldId': fieldId
    }
    
    return json.loads(requests.get(config['mrvUrl']+'/api/event-data',headers=header,params=data).text)
    

# %%
def fieldId(producerID, fieldName):
    
    header = refreshHeader()
    
    latestYear = fieldSummary(producerID,"9999")['latestYear']
    fields = fieldSummary(producerID,latestYear)
    fieldID = list(filter(lambda item: item['name'] == fieldName, fields['fields']))
    if len(fieldID) == 1: 
        return fieldID[0]['id']
    else:
        return None
    

# %%
def fieldSummary(producerId, year):

    global config
    assert(configIsValid())

    header = refreshHeader()
    
    data = {
        "excludeNoChange":"false",
        "selectedEnrollmentYear":year,
        "isEYearFieldsOnly":"false",
        "guest":producerId
    }

    return json.loads(requests.get(config['mrvUrl']+'/api/field/list',headers=header,params=data).text)


# %%
def myID():

    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    rsp = json.loads(requests.get(config['mrvUrl']+'/api/user/me',headers=header)._content)
    return (rsp['user']['id'])


# %%
def minmax():

    global config
    assert(configIsValid())

    header = refreshHeader()
    
    return (json.loads(requests.get(config['mrvUrl']+'/api/commodity-type',headers=header).text))
    
# %%
def OAuthTokenAndHeaders(authEmail="", authPassword=""):
    
    global config, openid, tokenRefresh
    assert(configIsValid())
    
    if not authEmail:
        authEmail = config['keycloakUser']
    if not authPassword:
        authPassword = config['keycloakPassword']
        
    # Get authorization token
    openid = KeycloakOpenID(server_url=config['keycloakAuthUrl'],client_id=config['keycloakClientId'],realm_name=config['keycloakRealmName'],
                            client_secret_key=config['keycloakClientSecret'])
    token = openid.token(authEmail,authPassword)
    tokenRefresh = token['refresh_token']
    
    # Standard header 
    headers = {
        "Authorization": "Bearer " + token['access_token'],
        "Content-Type": "application/json"
    }
    
    return (token['access_token'], headers)

# %%
def producerId(producerEmail, enrollmentYear):
        
    producer = userDetails(producerEmail, enrollmentYear)
    if producer:
        return producer['id']
    else:
        return None

# %%
def projectId(projectName):
    
    global config
    assert(configIsValid())
    
    projects = json.loads(requests.get(config['mrvUrl']+'/api/base/projects').text)
    projId = list(filter(lambda item: item['name'] == projectName, projects))
    if len(projId) == 1:
        return projId[0]['id']
    else:
        return None
    

# %%
def refreshHeader():
    
    # global openid
    # token = openid.refresh_token(tokenRefresh)
    # header = {
    #     "Authorization": "Bearer " + token['access_token'],
    #     "Content-Type": "application/json"
    # }
    # return header

    token, header = OAuthTokenAndHeaders()
    return header


# %%
def userDetails(producerEmail, enrollmentYear):
    
    global config
    assert(configIsValid())
    
    header = refreshHeader()
    
    urlParams = {
        'review': 'false',
        'selectedEnrollmentYear': enrollmentYear
    }
    payload = {
        'skip': '0',
        'take': '200000'
    }
    req = requests.post(config['mrvUrl']+'/api/project/enrolledProducers',headers=header,params=urlParams,json=payload)
    producers = json.loads(requests.post(config['mrvUrl']+'/api/project/enrolledProducers',headers=header,params=urlParams,json=payload).text)
    producerID = list(filter(lambda item: item['email'] == producerEmail, producers['data']))
    if len(producerID) == 1: 
        return producerID[0]
    else:
        return None
    
