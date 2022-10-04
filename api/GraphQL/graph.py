import requests
import json

# Get Project abbreviations 
url = "https://graphql.ecoharvest.ag/api/rest/project_names"
# add API credentials
header = {'x-hasura-admin-secret': 'EnterSecretHere'}
# call API
r = requests.get(url, headers=header)
print(r.json())

# get field data for GMP project 
url2 = "https://graphql.ecoharvest.ag/api/rest/fields"
payload = {'abbr': 'SCT'}
r = requests.get(url2, headers=header, params=payload)
#print(r.json())
fieldDic1 = r.json()['esmcProject'][0]
projectName = fieldDic1['name']
enrollmentYear = fieldDic1['currentEnrollmentYear']
# look at fields for 1 producer 
farmerId = fieldDic1['farmer_projects'][0]['farmerAppUserId']
fields = fieldDic1['farmer_projects'][0]['farmer_project_fields']
#print(fields)
fieldIdList = []
acreageList = []
coordList = []
for field in fields:
	# grab field IDs to query for more details 
	fieldIdList.append(field['field']['id'])
	acreageList.append(field['field']['acres'])
	# save field boundaries 
	coordList.append(field['field']['boundary']['coordinates'])
#print(fieldIdList)
# sum field acres 
print("Project Name: ", projectName)
print("FarmerID: ", farmerId)
print("Current Enrollment Year: ", enrollmentYear)
print("Producer: ", farmerId)
print("Number of Fields: ", len(fields))
print("Total Acreage: ", sum(acreageList))

# get enrollment year for field 
url3 = "https://graphql.ecoharvest.ag/api/rest/get_enrollment_year" 
pracChanges = []
# get practice change info for a single field 
url4 = "https://graphql.ecoharvest.ag/api/rest/getFieldPracticeChanges"
for i in fieldIdList:
	payload = {'fieldId': i}
	enrollment_obj = requests.get(url3, headers=header, params=payload)
	enrollment_year = enrollment_obj.json()['esmcFarmerProjectField'][0]['farmer_project']['enrollment_year']
	proj_name = enrollment_obj.json()['esmcFarmerProjectField'][0]['farmer_project']['project']['name']
	pracChangeDic = {}
	# pass in enrollment year 
	payload = {'fieldId': i,'year': enrollment_year}
	r = requests.get(url4, headers=header, params=payload)
	#print(r.json())
	pracChangeDic['id'] = i
	pracChangeDic['pracChange'] = r.json()['practiceChanges']
	pracChangeDic['project'] = proj_name
	# now put in enrollment year 
	pracChanges.append(pracChangeDic)


print("Practice Changes by Field")
for prac in pracChanges:
	print(prac['id'], " | ", prac['pracChange'], " | ", prac['project'])






