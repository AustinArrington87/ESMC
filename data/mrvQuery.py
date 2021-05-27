import json
# open JSON file
#f = open('Il_Corn_sample_with_soil_measurement_stratum_sample.json')
#f = open('ILCorn-Data-2020-2021-05-27.json')
f = open('TNCMN-Data-2021-05-27.json')
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
# total acres
totalAcres = []
# totalCropHarvest
totalHarvestCorn = []
totalHarvestSoy = []
totalHarvestWheat = []
totalHarvestAlfalfa = []
# STATUS Dictionaries
statusInProgress = {"ProducerID": [], "Status": [], "ProducerAgreement": []}
statusSubmitted = {"ProducerID": [], "Status": [], "ProducerAgreement": []}
cropDic = {"FieldID": [], "CropType": [], "Yield": []}
soilSampleDic = {"FieldID": [], "SoilMeas_ID": [], "sampleName": [], "Coords": [], "pH": [], "SOC": [], "BD": [], "sample_date": []}

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

        # current year yield 
        for l in k["crops"]:
            print(k["fieldByProjectId"], "| Area: ", k["area"], "| Type: ", l["type"], "| Yield: ", l["yield"])
            if l["type"] == "corn":
                totalHarvestCorn.append(l["yield"])
            if l["type"] == "soybean":
                totalHarvestSoy.append(l["yield"])
            if l["type"] == "wheat":
                totalHarvestWheat.append(l["yield"])
            if l["type"] == "alfalfa":
                totalHarvestAlfalfa.append(l["yield"])

            # write to acres list 
            totalAcres.append(k["area"])
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

        # soil stratum 
        try:
            print("Soil Stratum")
            print(k["soil_strata"])
        except:
            pass

        # soil samples

        try:
            print("Soil Samples")
            for l in k["soil_samples"]:
                print(k["fieldByProjectId"], "| soilSampleID: ", l["soil_measurement__id"], "| sampleName: ", l["name"], \
                 "| Coords: ", l["actual_point"]["geometry"]["coordinates"], "| pH: ", l["ph"], "| SOC: ", l["soil_organic_carbon"],
                 "| BD: ", l["bulk_density"], "| SampleDate: ", l["date_sampled"])

                 # write to soil sample Dic 
                soilSampleDic["FieldID"].append(k["fieldByProjectId"])
                soilSampleDic["SoilMeas_ID"].append(l["soil_measurement__id"])
                soilSampleDic["sampleName"].append(l["name"])
                soilSampleDic["Coords"].append(l["actual_point"]["geometry"]["coordinates"])
                soilSampleDic["pH"].append(l["ph"])
                soilSampleDic["SOC"].append(l["soil_organic_carbon"])
                soilSampleDic["BD"].append(l["bulk_density"])
                soilSampleDic["sample_date"].append(l["date_sampled"])
        except:
            pass

        print("-----------------------------------------------")

print("=======================================================")
print("STATUS CHECK: ", data["project"])
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
### TOTAL ACRES ###
print("Total Acres: ", round(sum(totalAcres),2))
#### TOTAL HARVEST
# remove Nulls from list 
totalHarvestCorn = filter(None, totalHarvestCorn)
totalHarvestSoy = filter(None, totalHarvestSoy)
totalHarvestWheat = filter(None, totalHarvestWheat)
totalHarvestAlfalfa = filter(None, totalHarvestAlfalfa)

try:
    print("Total Yield lbs/acre (CORN): ", sum(totalHarvestCorn))
except:
    pass
try:
    print("Total Yield lbs/acre (SOYBEAN): ", sum(totalHarvestSoy))
except:
    pass
try:
    print("Total Yield lbs/acre (WHEAT): ", sum(totalHarvestWheat))
except:
    pass
try:
    print("Total Yield lbs/acre (ALFALFA): ", sum(totalHarvestAlfalfa))
except:
    pass

### new practices 
#print("New Practices: ", newPractices)
### no new practices
print("Still missing What's New: ", noNewPracticeClean)

#### CROP STATS #######
# find frequency of string in list 
def countCrop(lst, x):
    return lst.count(x)
# enter your crops 
crops = ["corn", "soybean", "wheat", "alfalfa"]
for crop in crops:
    print('{} grown on {} fields'.format(crop, countCrop(cropList, crop))) 

#### SOIL SAMPLE STATS ####

try:
    print("Soil Sample Summary:")
    print(soilSampleDic)
except:
    pass
