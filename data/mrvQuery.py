import json
# open JSON file
#f = open('Il_Corn_sample_with_soil_measurement_stratum_sample.json')
f = open('ILCorn-Data-2020-2021-05-27.json')
#f = open('TNCMN-Data-2021-05-27.json')
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
# missing historical practices
missingHistoricalPractices = []
# store producers with no new practices
noHistoricalPractices = []
noNewPractice = []
# total acres
totalAcres = []
# total producers
totalProducers = []
# totalCropHarvest
totalHarvestCorn = []
totalHarvestSoy = []
totalHarvestWheat = []
totalHarvestAlfalfa = []
fieldsWithNullHarvest = []
rotations = []
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
    totalProducers.append(i["userByProjectId"])
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
            
            # current year crop to compare with rotation context 
            
            rotations.append([i["userByProjectId"], k["fieldByProjectId"], l["type"], l["growingSeason"]["year"]])
            
            # harvest per crop 
            if l["type"] == "corn":
                totalHarvestCorn.append(l["yield"])
            if l["type"] == "soybean":
                totalHarvestSoy.append(l["yield"])
            if l["type"] == "wheat":
                totalHarvestWheat.append(l["yield"])
            if l["type"] == "alfalfa":
                totalHarvestAlfalfa.append(l["yield"])
            
            if l["yield"] == None:
                print("Missing yield data for ", l["type"], "in field: ", k["fieldByProjectId"])
                fieldsWithNullHarvest.append([i["userByProjectId"], k["fieldByProjectId"], l["type"]])

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
        
        # check historical practices -3 year (2017) to -1 (2019)
        try:
            if k["historicalPractices"][0]["yield"] == None:
                missingHistoricalPractices.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][0]["year"]])
            else:
                rotations.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][0]["crop"], k["historicalPractices"][0]["year"]])
            
            if k["historicalPractices"][1]["yield"] == None:
                missingHistoricalPractices.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][1]["year"]])
            else:
                rotations.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][1]["crop"], k["historicalPractices"][1]["year"]])
                
            if k["historicalPractices"][2]["yield"] == None:
                missingHistoricalPractices.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][2]["year"]])
            else:
                rotations.append([i["userByProjectId"], k["fieldByProjectId"], k["historicalPractices"][2]["crop"], k["historicalPractices"][2]["year"]])
            
        except:
            pass
        
        # if it's an empty list 
        if not k["historicalPractices"]:
            noHistoricalPractices.append([i["userByProjectId"], k["fieldByProjectId"]])

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

print("====================PROJECT SUMMARY===================================")
print("PILOT PROJECT: ", data["project"])
print("ASSETS: ", data["assets"])
### new practices 
print("WHAT'S NEW? : ", newPractices)
print("======================STATUS==========================================")
unique = set(statusCheck)
for item in unique:
    if item == "Submitted":
        print(item, "|", statusCheck.count(item), "|", statusSubmitted["ProducerID"], "| SignedAgreement:", statusSubmitted["ProducerAgreement"])
    else:
        print(item, "|", statusCheck.count(item), "|", statusInProgress["ProducerID"], "| SignedAgreement:", statusInProgress["ProducerAgreement"])

cropList = cropDic["CropType"]
fieldList = cropDic["FieldID"]

### FIELD STATS #### 
print("Total Producers: ", len(totalProducers))
print("Total Fields: ", len(fieldList))
### TOTAL ACRES ###
print("Total Acres: ", round(sum(totalAcres),2))
#### CROP ROTATIONS #### 

for i in rotations:
    for j in missingHistoricalPractices:
        if i[0] == j[0] and i[1] == j[1]:
            rotations.remove(i)

print("Crop Rotation: ", rotations)

for x in totalProducers:
    for y in fieldList:
        for z in rotations:
            if x == z[0] and y == z[1]:
                print(x, z)

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

#### CROP STATS #######
# find frequency of string in list 
def countCrop(lst, x):
    return lst.count(x)
# enter your crops 
crops = ["corn", "soybean", "wheat", "alfalfa"]
for crop in crops:
    print('{} grown on {} fields'.format(crop, countCrop(cropList, crop))) 

print("======================MISSING DATA=====================================")
# fields with null Harvest
print("Fields with Missing Yield: ", fieldsWithNullHarvest)

# fields with missing historical crop data 
print("Fields with Missing Historical: ", missingHistoricalPractices)
# fields with no historical
print("Fields with No Historical: ", noHistoricalPractices)

### no new practices
print("Still missing What's New: ", noNewPracticeClean)


#### SOIL SAMPLE STATS ####
print("======================SOIL SAMPLE SUMMARY==============================")

try:
    print("Soil Sample Summary:")
    print(soilSampleDic)
except:
    pass
