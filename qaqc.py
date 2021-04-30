import json
# open JSON file
#f = open('GM-2020-Fields-2021-04-29.json',)
#f = open('ILC-2020-Fields-2021-04-29.json',)
#f = open('TNCMN-2020-Fields-2021-04-29.json',)
f = open('GM-ILC-TNCMN-2020-Fields-2021-04-29.json')
# retrun JSON obj as dictionary 
projects = json.load(f)
# general mills
gmProducers = []
# IL Corn
ILProducers = []
# TNC MN
tncProducers = []
# print project names
for i in projects:
    #print("PILOT PROJECTS")
    print(i["project"])
    if i["project"] == "General Mills Project":
        gmProducers.append(i["producers"])
    elif i["project"] == "Illinois Corn Growers Project":
        ILProducers.append(i["producers"])
    elif i["project"] == "TNC Minnesota Project":
        tncProducers.append(i["producers"])
        
print("=======================================")


def qualityControl(pilotName, pilotData, knownProducers, knownFields):
    ProducersNo = pilotData[0]
    ProducerEntered = len(ProducersNo)
    # Expected Values 
    print(pilotName, "| Known Producers: ", knownProducers)
    print(pilotName, "| Known Fields: ", knownFields)
    
    # Detected Producers 
    print(pilotName, "| number of detected producers: ", ProducerEntered)
    
    if knownProducers == ProducerEntered:
        print(pilotName, "| producer number PASSED")
    else:
        print(pilotName, "| producer number FAILED")
    
    fields = []
    for i in ProducersNo:
        fields.append(i["fields"])
    fieldSum = []
    for i in fields:
        fieldSum.append(len(i))
    
    totalFields = sum(fieldSum)
    
    print(pilotName, "| number of detected fields: ", totalFields)
    if knownFields == totalFields:
        print(pilotName, "| field number PASSED")
    else:
        print(pilotName, "| producer number FAILED")
    
    return pilotName, "Analysis Complete"


# Feed data through function 
# General Mills 
pilotName = "General Mills Project"
gmKnownProducers = 21
gmKnownFields = 94
print(qualityControl(pilotName, gmProducers, gmKnownProducers, gmKnownFields))

#IL Corn 
pilotName = "Illinois Corn Growers Project"
ILKnownProducers = 10
ILKnownFields = 34
print(qualityControl(pilotName, ILProducers, ILKnownProducers, ILKnownFields))

# TNC MN
pilotName = "TNC Minnesota Project"
tncKnownProducers = 4
tncKnownFields = 4
print(qualityControl(pilotName, tncProducers, tncKnownProducers, tncKnownFields))

