import json
# open JSON file
#f = open('IL-Corn-Data-2021-03-11.json',)
#f = open('IL-Corn-Data-2021-05-11-without-fields-24-25.json')
f = open('IL-Corn-Data-2021-05-24.json')
#f = open('anonymized_data-2021-02-15.json',)
# retrun JSON obj as dictionary 
data = json.load(f)[0]
# Project Name
print("Project: ", data["project"])
# Date Added
print("Date Added: ", data["date"])
# Number of Producers
print("Number of Producers: ", len(data["producers"]))
# check Status Later 
statusCheck = []
# store whats new values
newPractices = []
# store producers with no new practices
noNewPractice = []

statusInProgress = {"ProducerID": [], "Status": [], "ProducerAgreement": []}
statusSubmitted = {"ProducerID": [], "Status": [], "ProducerAgreement": []}
cropDic = {"FieldID": [], "CropType": [], "Yield": []}
# iterate through Producers 
for i in data["producers"]:
    # check status 
    statusCheck.append(i["status"])
    if i["status"] == "Submitted":
        statusSubmitted["Status"].append(i["status"])
        statusSubmitted["ProducerID"].append(i["userByProjectId"])
        statusSubmitted["ProducerAgreement"].append(i["has_agreed_to_producer_agreement"])
    else:
        statusInProgress["Status"].append(i["status"])
        statusInProgress["ProducerID"].append(i["userByProjectId"])
        statusInProgress["ProducerAgreement"].append(i["has_agreed_to_producer_agreement"])
    
    # Producer ID 
    print(i["userByProjectId"])
    # historical yields crop
    print("Historical Yields")
    histYields = i["narrative"]["historical_yields"]
    #print(histYields)
    for j in histYields:
        print(j["crop"], "| Year 1: ", j["yield_1"], "| Year 2: ", j["yield_2"], "| Year 3: ", j["yield_3"])
    # Fields
    print("Fields")
    fields = i["fields"]
    # what's new 
    for k in fields:

        # historical crop practices 
        for l in k["crops"]:
            print(k["fieldByProjectId"], "| Area: ", k["area"], "| Type: ", l["type"], "| Yield: ", l["yield"])
            # write Crop Dictionary 
            cropDic["FieldID"].append(k["fieldByProjectId"])
            cropDic["CropType"].append(l["type"])
            cropDic["Yield"].append(l["yield"])

        print("What's New: ", k["whatsNew"])
        if k["whatsNew"]["nutrientManagement"] == None:
            print("No new nutrient management practice")
        else:
            newPractices.append([i["userByProjectId"], k["fieldByProjectId"], "nutrientManagement"])
        if k["whatsNew"]["coverCrop"] == None:
            print("No new cover crop practices")
        else:
            newPractices.append([i["userByProjectId"], k["fieldByProjectId"],"coverCrop"])
        if k["whatsNew"]["conservationPractices"] == None:
            print("No new conservation practices")
        else:
            newPractices.append([i["userByProjectId"], k["fieldByProjectId"], "conservationPractices"])
        if k["whatsNew"]["tillage"] == None:
            print("No new tillage practices")
        else:
            newPractices.append([i["userByProjectId"], k["fieldByProjectId"], "tillage"])
        if k["whatsNew"]["prescribedGrazing"] == None:
            print("No new prescribed grazing practices")
        else:
            newPractices.append([i["userByProjectId"], k["fieldByProjectId"], "prescribedGrazing"])
        
        # check if no new practices added 
        if k["whatsNew"]["nutrientManagement"] == None and \
            k["whatsNew"]["coverCrop"] == None and \
            k["whatsNew"]["conservationPractices"] == None and \
            k["whatsNew"]["tillage"] == None and \
            k["whatsNew"]["prescribedGrazing"] == None:
            noNewPractice.append(i["userByProjectId"])
            noNewPracticeClean = []
            [noNewPracticeClean.append(x) for x in noNewPractice if x not in noNewPracticeClean]


        print("-----------------------------------------------")

print("=======================================================")
print("STATUS CHECK")
unique = set(statusCheck)
for item in unique:
    if item == "Submitted":
        print(item, "|", statusCheck.count(item), "|", statusSubmitted["ProducerID"], "| SignedAgreement:", statusSubmitted["ProducerAgreement"])
    else:
        print(item, "|", statusCheck.count(item), "|", statusInProgress["ProducerID"], "| SignedAgreement:", statusInProgress["ProducerAgreement"])

cropList = cropDic["CropType"]
fieldList = cropDic["FieldID"]

### FIELD STATS #### 
print("Total Fields: ", len(fieldList))
### new practices 
print("New Practices: ", newPractices)
### no new practices
print("Still missing What's New: ", noNewPracticeClean)
#### CROP STATS #######
# find frequency of string in list 
def countCrop(lst, x):
    return lst.count(x)
# enter your crops 
crops = ["corn", "soybean", "wheat"]
for crop in crops:
    print('{} grown on {} fields'.format(crop, countCrop(cropList, crop)))

### FIELD STATS #### 
print("Total Fields: ", len(fieldList))
#### CROP STATS #######
# find frequency of string in list 
def countCrop(lst, x):
    return lst.count(x)
# enter your crops 
crops = ["corn", "soybean", "wheat"]
for crop in crops:
    print('{} grown on {} fields'.format(crop, countCrop(cropList, crop))) 
