import csv
import pandas as pd
import numpy as np

pd.set_option("display.max_colwidth", 10000)

enrollment_year = 2021
eyMin1 = enrollment_year-1
eyMin2 = enrollment_year-2
eyMin3 = enrollment_year-3
project_years = [enrollment_year, eyMin1, eyMin2, eyMin3]
optis_lookback = [enrollment_year-4, enrollment_year-5, enrollment_year-6]
field_ids = []
crops = []
projects = []
# put the "bad fields" with historical cover crops caught in Optis, not recorded in MRV
bad_fields_cc = []
bad_fields_tillage = []

# Load Data
file1 = 'mrv_data.csv'
file2 = 'optis_data.csv'
project_name = "Benson_Hill"

# dump your merged MRV-Optis data frames here 
dataBucket = []

# for additional OpTIS lookback
optisLookback = []

def unique(list1):
	x = np.array(list1)
	return(np.unique(x))

def MergeDataByYear (season, project, mrv_file, opt_file):

	df_mrv = pd.read_csv(mrv_file, usecols = ['project_name', 'producer_name', 'id', 'field_name', 'acres',
		'initial_year', 'season', 'practice_name', 'crop_name'])

	df_opt = pd.read_csv(opt_file, usecols = ['Name', 'Id', 'source', 'year', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name'])

	crops = df_mrv['crop_name']
	crop_list = crops.to_list()
	crop_list_unique = unique(crop_list)
	print(crop_list_unique)

	# unique field IDs (remove duplicate rows from fields with multiple practice changes)
	ids = df_mrv['id']
	id_list = ids.to_list()
	id_list_unique = unique(id_list)
	print(id_list_unique)
	field_ids.append(id_list_unique)

	# projects 
	projects = df_mrv['project_name']
	project_list = projects.to_list()
	project_list_unique = unique(project_list)
	print(project_list_unique)

	# noralize project names between OpTis and MRV 
	if project == "Benson_Hill":
		mrv_projName = "Benson Hill"
		opt_projName = "Benson Hill 2021 Fields"

	MRVprojectFrame = df_mrv.loc[df_mrv['project_name'] == mrv_projName]
	MRVprojFrameByYear = MRVprojectFrame[MRVprojectFrame['season'] == season]
	OPTprojectFrame = df_opt.loc[df_opt['source'] == opt_projName]
	OPTprojFrameByYear = OPTprojectFrame[OPTprojectFrame['year'] == season]

	MRV_Opt_Merged = MRVprojFrameByYear.merge(OPTprojFrameByYear, left_on="id", right_on='Id')[['project_name', 'producer_name', 'id', 'field_name', 
	'acres', 'initial_year', 'year', 'practice_name', 'crop_name', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name']]

	dataBucket.append(MRV_Opt_Merged)
	# export CSV

def OPT (season, project, opt_file):

	df_opt = pd.read_csv(opt_file, usecols = ['Name', 'Id', 'source', 'year', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name'])

	# isolate Benson Hills MRV project 
	if project == "Benson_Hill":
		opt_projName = "Benson Hill 2021 Fields"

	OPTprojectFrame = df_opt.loc[df_opt['source'] == opt_projName]
	OPTprojFrameByYear = OPTprojectFrame[OPTprojectFrame['year'] == season]
	optisLookback.append(OPTprojFrameByYear)

# call function and export CSVs 
for year in project_years:
	MergeDataByYear(year, project_name, file1, file2)

# OpTIS lookback 
for year in optis_lookback:
	OPT(year, project_name, file2)

# normalize data 
for d in dataBucket:
	# replace "Corn, Grain" with "Corn" in MRV data
	d['crop_name'] = d['crop_name'].str.replace('Corn, Grain', 'Corn')

# enrollment year data, index 0 in dataBucket 
# 2021 year
dataEnrollment = dataBucket[0]
# 2020 (2021 minus 1)
dataEnrollmentMin1 = dataBucket[1]
#2019 (2021 minus 2)
dataEnrollmentMin2 = dataBucket[2]
#2018 (2021 minus 3)
dataEnrollmentMin3 = dataBucket[3]

print(dataEnrollment)
print(dataEnrollmentMin1)
print(dataEnrollmentMin2)
print(dataEnrollmentMin3)

mrv_CDL_errors = []
# check if crops are equal from MRV to Optis / CDL 
mrvCDL_0 = dataEnrollment['crop_name'].equals(dataEnrollment['name'])
mrvCDL_1 = dataEnrollmentMin1['crop_name'].equals(dataEnrollmentMin1['name'])
mrvCDL_2 = dataEnrollmentMin2['crop_name'].equals(dataEnrollmentMin2['name'])
mrvCDL_3 = dataEnrollmentMin3['crop_name'].equals(dataEnrollmentMin3['name'])

# check when is last year crop grown 
cropYearMin1 = dataEnrollment['crop_name'].equals(dataEnrollmentMin1['crop_name'])
cropYearMin2 = dataEnrollment['crop_name'].equals(dataEnrollmentMin2['crop_name'])
cropYearMin3 = dataEnrollment['crop_name'].equals(dataEnrollmentMin3['crop_name'])

if cropYearMin1 == True:
	LastCropYear = project_years[1]
	NullFallTillMin1 = dataEnrollmentMin1['fall_till_class'].isna().sum()
	NullSpringTillMin1 = dataEnrollmentMin1['spring_till_class'].isna().sum()
elif cropYearMin2 == True:
	LastCropYear = project_years[2]
	NullFallTillMin2 = dataEnrollmentMin2['fall_till_class'].isna().sum()
	NullSpringTillMin2 = dataEnrollmentMin2['spring_till_class'].isna().sum()
elif cropYearMin3 == True:
	LastCropYear = project_years[3]
	NullFallTillMin3 = dataEnrollmentMin3['fall_till_class'].isna().sum()
	NullSpringTillMin3 = dataEnrollmentMin3['spring_till_class'].isna().sum()
else:
	LastCropYear = None

# check for acreage, reference field ID list 
print(dataEnrollment['id'])
print(dataEnrollment['acres'])
print("""
------------------------------OpTIS Report----------------------------------- 
""")
print("Project Name: " + project_name)
# count rows 
row_count, col_count = dataEnrollment.shape
# Field count
print("Total Fields: ", row_count)
# sum acres 
print("Total Acres: ", dataEnrollment['acres'].sum())

# check if full rotation was captured, and wwhat is the last year crop was grown 
if LastCropYear == None:
	print("Full Crop Rotation Not Captured")
else:
	print("Last Crop Year for Practice Change Check:", LastCropYear)

print("Practice Changes & Commodity Crop by Field")
print(dataEnrollment['field_name']+" ("+dataEnrollment['id']+")"+": "+dataEnrollment['practice_name'])
print(dataEnrollment['field_name']+" ("+dataEnrollment['id']+"): "+dataEnrollment['crop_name'])

# sum nulls in OpTIS data. Most likely areas where cloud cover obscures satallite image
# OpTIS Performance Analysis
NullFallTill = dataEnrollment['fall_till_class'].isna().sum()
NullSpringTill = dataEnrollment['spring_till_class'].isna().sum()
NullCC = dataEnrollment['cover_crop'].isna().sum()
percentFallTillNull = NullFallTill/row_count
percentSpringTillNull = NullSpringTill/row_count
percentCCNull = NullCC/row_count
print("Percent of Fields with missing 2021 Fall Tillage Estimates: " +str(percentFallTillNull*100)+"%")
print("Percent of Fields with missing 2021 Spring Tillage Estimates: "+str(percentSpringTillNull*100)+"%")
print("Percent of Fields with missing 2021 Cover Crop Estimates: "+str(percentCCNull*100)+"%")
print("""
------------------------------------------------------------------------------ 
""")

print("OpTIS CDL to MRV Crop Check")

if mrvCDL_0 == True:
	print("2021 MRV and CDL Pass Check")
else:
	print("2021 MRV and CDL Fail Check")
	mrv_CDL_errors.append(project_years[0])
if mrvCDL_1 == True:
	print("2020 MRV and CDL Pass Check")
else:
	print("2020 MRV and CDL Fail Check")
	mrv_CDL_errors.append(project_years[1])
if mrvCDL_2 == True:
	print("2019 MRV and CDL Pass Check")
else:
	print("2019 MRV and CDL Fail Check")
	mrv_CDL_errors.append(project_years[2])
if mrvCDL_3 == True:
	print("2018 MRV and CDL Pass Check")
else:
	print("2018 MRV and CDL Fail Check")
	mrv_CDL_errors.append(project_years[3])

print("""
------------------------------------------------------------------------------ 
""")
# TILLAGE 
projectTillStatus = "Passed"
projectPracticeStatus = "Passed"
projectCoverCropStatus = "Passed"

if percentFallTillNull >= 0.5:

	projectTillStatus = """

Failed

At least half of the fields are missing Fall Tillage data for the enrollment year. 
"""

if percentSpringTillNull >= 0.5:

	projectTillStatus = """
Failed

At least half of the fields are missing Spring Tillage data for the enrollment year. 
"""

if percentSpringTillNull >= 0.5 and percentFallTillNull >= 0.5:

	projectTillStatus = """

Failed

At least half of the fields are missing both Spring and Fall Tillage data for the enrollment year. 
"""

# check for tillage practice change eligibility. If they are doing tillage reduction,
# should not have feilds with conventional till in the practice change year 

if dataEnrollment['practice_name'].str.contains('Tillage').any():
	bad_fields_tillage.append(dataEnrollment.loc[dataEnrollment['fall_till_class'] == 1, 'id'])
	bad_fields_tillage.append(dataEnrollment.loc[dataEnrollment['spring_till_class'] == 1, 'id'])

print("OpTIS Tillage Eligibility: " + projectTillStatus)

for b in bad_fields_tillage:
	if b.empty == True:
		pass
	else:
		print("There are fields in the enrollment year with conventional tillage flagged by OpTIS, but tillage reduction is assigned as a practice change.")
		print("Fields with OpTIS / MRV tillage incongruencies")
		print(b)

### END TILLAGE SECTION 

###################################
# PRACTICE CHANGE - Determine when last time commodity crop was grown 
print("""
------------------------------------------------------------------------------ 
""")
if LastCropYear == eyMin1:
	percentFallTillNull_Prac = NullFallTillMin1/row_count
	percentSpringTillNull_Prac = NullSpringTillMin1/row_count
	coverCropCountLastCropYear = dataEnrollmentMin1['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin1.loc[dataEnrollmentMin1['cover_crop'] >= 1, 'id'])
if LastCropYear == eyMin2:
	# tillage 
	percentFallTillNull_Prac = NullFallTillMin2/row_count
	percentSpringTillNull_Prac = NullSpringTillMin2/row_count
	# cover cropping
	coverCropCountLastCropYear = dataEnrollmentMin2['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin2.loc[dataEnrollmentMin2['cover_crop'] >= 1, 'id'])
if LastCropYear == eyMin3:
	percentFallTillNull_Prac = NullFallTillMin3/row_count
	percentSpringTillNull_Prac = NullSpringTillMin3/row_count
	coverCropCountLastCropYear = dataEnrollmentMin3['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin3.loc[dataEnrollmentMin3['cover_crop'] >= 1, 'id'])

# cover crop eligibility check 
if dataEnrollment['practice_name'].str.contains('Cover').any():
	#print(coverCropCountLastCropYear)
	if coverCropCountLastCropYear >= 1:
		projectCoverCropStatus = """
Failed

In the last year this crop was grown, OpTis flags cover crop occurrence. 
However, Cover Cropping is listed as a practice change.
"""

if percentCCNull >= 0.5:

	projectCCStatusNull = """

At least half of the fields are missing cover crop data for the enrollment year. 
"""
else:
	projectCCStatusNull = ""

print("OpTIS Cover Cropping Eligibility: " + projectCoverCropStatus+projectCCStatusNull)

for b in bad_fields_cc:
	if b.empty == True:
		pass
	else:
		print("Fields with OpTIS / cover crop incongruencies")
		print(b)

print("""
------------------------------------------------------------------------------ 
""")

# Written by Austin Arrington. Copyright 2022 ESMC
