import json
# open JSON file
f = open('IL-Corn-Data-2021-03-11.json',)
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
#statusSubmitted = []
statusInProgress = {"ProducerID": [], "Status": []}
statusSubmitted = {"ProducerID": [], "Status": []}

# iterate through Producers 
for i in data["producers"]:
    # check status 
    statusCheck.append(i["narrative"]["status"])
    if i["narrative"]["status"] == "Submitted":
        statusSubmitted["Status"].append(i["narrative"]["status"])
        statusSubmitted["ProducerID"].append(i["userByProjectId"])
    else:
        statusInProgress["Status"].append(i["narrative"]["status"])
        statusInProgress["ProducerID"].append(i["userByProjectId"])
    
    # Producer ID 
    print(i["userByProjectId"])
    # historical yields crop
    print("Historical Yields")
    histYields = i["narrative"]["historical_yields"]
    #print(histYields)
    for j in histYields:
        print(j["commodity__id"], "| Year 1: ", j["yield_1"], "| Year 2: ", j["yield_2"], "| Year 3: ", j["yield_3"])
    # Fields
    print("Fields")
    fields = i["fields"]
    for k in fields:
        print(k["fieldByProjectId"])
    print("==================")

print("--------------------------------------------------------")
print("STATUS CHECK")
unique = set(statusCheck)
for item in unique:
    if item == "Submitted":
        print(item, "|", statusCheck.count(item), "|", statusSubmitted["ProducerID"])
    else:
        print(item, "|", statusCheck.count(item), "|", statusInProgress["ProducerID"])
        

        
        
