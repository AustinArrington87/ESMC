import csv
import pandas as pd
import numpy as np

# Cover Crop Key
# 0 - no winter cover
# 1 - cover crop (full season or general)
# 2 - winter commodity crop 
# Null - No data
# If conf_index_cover_crop <= 0.7, ignore OpTIS.

# Fall and Spring Tillage Key
# 1 - Conventional Tillage
# 2 - Reduced Till
# 3 - No Till
# Null - No data
# If conf_index_spring_tillage or conf_index_fall_tillage <= 40, ignore OpTIS.

pd.set_option("display.max_colwidth", 10000)

enrollment_year = 2021
eyMin1 = enrollment_year-1
eyMin2 = enrollment_year-2
eyMin3 = enrollment_year-3
eyMin4 = enrollment_year-4
eyMin5 = enrollment_year-5
eyMin6 = enrollment_year-6
project_years = [enrollment_year, eyMin1, eyMin2, eyMin3]
optis_lookback = [eyMin4, eyMin5, eyMin6]
field_ids = []
crops = []
projects = []
# put the "bad fields" with historical cover crops caught in Optis, not recorded in MRV
bad_fields_cc = []
bad_fields_tillage = []
bad_fields_tillage1 = []
bad_fields_tillage2 = []
bad_fields_tillage3 = []

# Load Data
file1 = 'mrv_data.csv'
file2 = 'optis_data.csv'
project_name = "Benson_Hill"
#project_name = "Corteva"
#project_name = "Corteva_Nutrien"
#project_name = "General_Mills"
#project_name = "IL_Corn"
#project_name = "MOCS"
#project_name = "TNC_MN"

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
	if project == "Corteva":
		mrv_projName = "Corteva"
		opt_projName = "Corteva 2021 Fields"
	if project == "Corteva_Nutrien":
		mrv_projName = "Corteva-Nutrien"
		opt_projName = "Corteva-Nutrien 2021 Fields"
	if project == "General_Mills":
		mrv_projName = "General Mills"
		opt_projName = "General Mills 2021 Fields"
	if project == "IL_Corn":
		mrv_projName = "Illinois Corn Growers"
		opt_projName = "ICG 2021 Fields"
	if project == "MOCS":
		mrv_projName = "Missouri Partnership Pilot"
		opt_projName = "MOCS 2021 Fields"
	if project == "TNC_MN":
		mrv_projName = "TNC Minnesota"
		opt_projName = "TNC MN 2021 Fields"

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
	if project == "Corteva":
		opt_projName = "Corteva 2021 Fields"
	if project == "Corteva_Nutrien":
		mrv_projName = "Corteva-Nutrien"
		opt_projName = "Corteva-Nutrien 2021 Fields"
	if project == "General_Mills":
		mrv_projName = "General Mills"
		opt_projName = "General Mills 2021 Fields"
	if project == "IL_Corn":
		mrv_projName = "Illinois Corn Growers"
		opt_projName = "ICG 2021 Fields"
	if project == "MOCS":
		mrv_projName = "Missouri Partnership Pilot"
		opt_projName = "MOCS 2021 Fields"
	if project == "TNC_MN":
		mrv_projName = "TNC Minnesota"
		opt_projName = "TNC MN 2021 Fields"

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
	d['crop_name'] = d['crop_name'].str.replace('Corn, Silage', 'Corn')
	d['crop_name'] = d['crop_name'].str.replace('Wheat, Winter', 'Winter Wheat')
	d['crop_name'] = d['crop_name'].str.replace('Wheat, Spring', 'Spring Wheat')
	d['crop_name'] = d['crop_name'].str.replace('Sorghum, Grain', 'Sorghum')


# enrollment year data, index 0 in dataBucket 
# 2021 year
dataEnrollment = dataBucket[0]
# 2020 (2021 minus 1)
dataEnrollmentMin1 = dataBucket[1]
#2019 (2021 minus 2)
dataEnrollmentMin2 = dataBucket[2]
#2018 (2021 minus 3)
dataEnrollmentMin3 = dataBucket[3]
#2017
dataEnrollmentMin4 = optisLookback[0]
#2016
dataEnrollmentMin5 = optisLookback[1]
#2015
dataEnrollmentMin6 = optisLookback[2]

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
cropYearMin4 = dataEnrollment['crop_name'].equals(dataEnrollmentMin4['name'])
cropYearMin5 = dataEnrollment['crop_name'].equals(dataEnrollmentMin5['name'])
cropYearMin6 = dataEnrollment['crop_name'].equals(dataEnrollmentMin6['name'])

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

# optis lookback
if cropYearMin4 == True:
	LookBackYear = optis_lookback[0]
if cropYearMin5 == True:
	LookBackYear = optis_lookback[1]
if cropYearMin6 == True:
	LookBackYear = optis_lookback[2]
else:
	LookBackYear = None

# check for acreage, reference field ID list 
#print(dataEnrollment['id'])
#print(dataEnrollment['acres'])
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

print("Practice Changes by Field")
print(dataEnrollment['field_name'].values+" ("+dataEnrollment['id'].values+")"+": "+dataEnrollment['practice_name'].values)
print("Commodity Crop by Field")
print(dataEnrollment['field_name'].values+" ("+dataEnrollment['id'].values+"): "+dataEnrollment['crop_name'].values)
print("--------------------------------------------------------------------")
# sum nulls in OpTIS data. Most likely areas where cloud cover obscures satallite image
# OpTIS Performance Analysis
NullFallTill = dataEnrollment['fall_till_class'].isna().sum()
NullSpringTill = dataEnrollment['spring_till_class'].isna().sum()
NullCC = dataEnrollment['cover_crop'].isna().sum()
percentFallTillNull = NullFallTill/row_count
percentSpringTillNull = NullSpringTill/row_count
percentCCNull = NullCC/row_count
print("NULL Values in Project Year:")
print("Percent of Fields with missing 2021 Fall Tillage Estimates: " +str(round(percentFallTillNull*100, 2))+"%")
print("Percent of Fields with missing 2021 Spring Tillage Estimates: "+str(round(percentSpringTillNull*100, 2))+"%")
print("Percent of Fields with missing 2021 Cover Crop Estimates: "+str(round(percentCCNull*100, 2))+"%")
print("--------------------------------------------------------------------")
cc_fail1 = []
cc_fail2 = []
cc_fail3 = []
cc_fail4 = []
cc_fail5 = []
cc_fail6 = []
cc_fail7 = []
cc_fail1.append(dataEnrollment.loc[dataEnrollment['conf_index_cover_crop'] <= 0.7, 'id'].values)
cc_fail2.append(dataEnrollmentMin1.loc[dataEnrollmentMin1['conf_index_cover_crop'] <= 0.7, 'id'].values)
cc_fail3.append(dataEnrollmentMin2.loc[dataEnrollmentMin2['conf_index_cover_crop'] <= 0.7, 'id'].values)
cc_fail4.append(dataEnrollmentMin3.loc[dataEnrollmentMin3['conf_index_cover_crop'] <= 0.7, 'id'].values)
cc_fail5.append(dataEnrollmentMin4.loc[dataEnrollmentMin4['conf_index_cover_crop'] <= 0.7, 'Id'].values)
cc_fail6.append(dataEnrollmentMin5.loc[dataEnrollmentMin5['conf_index_cover_crop'] <= 0.7, 'Id'].values)
cc_fail7.append(dataEnrollmentMin6.loc[dataEnrollmentMin6['conf_index_cover_crop'] <= 0.7, 'Id'].values)
cc_fail1 = unique(cc_fail1)
cc_fail2 = unique(cc_fail2)
cc_fail3 = unique(cc_fail3)
cc_fail4 = unique(cc_fail4)
cc_fail5 = unique(cc_fail5)
cc_fail6 = unique(cc_fail6)
cc_fail7 = unique(cc_fail7)

if cc_fail1.any():
	print(str(enrollment_year)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail1)
	percent_CC_ConfFail = len(cc_fail1)/row_count
	print("Percent of "+str(enrollment_year)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(enrollment_year)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail2.any():
	print(str(eyMin1)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail2)
	percent_CC_ConfFail = len(cc_fail2)/row_count
	print("Percent of "+str(eyMin1)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin1)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail3.any():
	print(str(eyMin2)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail3)
	percent_CC_ConfFail = len(cc_fail3)/row_count
	print("Percent of "+str(eyMin2)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin2)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail4.any():
	print(str(eyMin3)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail4)
	percent_CC_ConfFail = len(cc_fail4)/row_count
	print("Percent of "+str(eyMin3)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin3)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail5.any():
	print(str(eyMin4)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail5)
	percent_CC_ConfFail = len(cc_fail5)/row_count
	print("Percent of "+str(eyMin4)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin4)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail6.any():
	print(str(eyMin5)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail6)
	percent_CC_ConfFail = len(cc_fail6)/row_count
	print("Percent of "+str(eyMin5)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin5)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")

if cc_fail7.any():
	print(str(eyMin6)+" Fields with Failed Cover Crop Confidence Index:")
	print(cc_fail7)
	percent_CC_ConfFail = len(cc_fail7)/row_count
	print("Percent of "+str(eyMin6)+" Fields with Failed Cover Crop Confidence Index: " +str(round(percent_CC_ConfFail*100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin6)+" Fields Pass Cover Crop Confidence Index")
	print("--------------------------------------------------------------------")


# till confidence check 

Falltill_fail1 = []
Falltill_fail2 = []
Falltill_fail3 = []
Falltill_fail4 = []
Falltill_fail5 = []
Falltill_fail6 = []
Falltill_fail7 = []
Falltill_fail1.append(dataEnrollment.loc[dataEnrollment['conf_index_fall_res'] <= 40, 'id'].values)
Falltill_fail2.append(dataEnrollmentMin1.loc[dataEnrollmentMin1['conf_index_fall_res'] <= 40, 'id'].values)
Falltill_fail3.append(dataEnrollmentMin2.loc[dataEnrollmentMin2['conf_index_fall_res'] <= 40, 'id'].values)
Falltill_fail4.append(dataEnrollmentMin3.loc[dataEnrollmentMin3['conf_index_fall_res'] <= 40, 'id'].values)
Falltill_fail5.append(dataEnrollmentMin4.loc[dataEnrollmentMin4['conf_index_fall_res'] <= 40, 'Id'].values)
Falltill_fail6.append(dataEnrollmentMin5.loc[dataEnrollmentMin5['conf_index_fall_res'] <= 40, 'Id'].values)
Falltill_fail7.append(dataEnrollmentMin6.loc[dataEnrollmentMin6['conf_index_fall_res'] <= 40, 'Id'].values)
Falltill_fail1 = unique(Falltill_fail1)
Falltill_fail2 = unique(Falltill_fail2)
Falltill_fail3 = unique(Falltill_fail3)
Falltill_fail4 = unique(Falltill_fail4)
Falltill_fail5 = unique(Falltill_fail5)
Falltill_fail6 = unique(Falltill_fail6)
Falltill_fail7 = unique(Falltill_fail7)


if Falltill_fail1.any():
	print(str(enrollment_year)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail1)
	percent_FallTill_ConfFail = len(Falltill_fail1)/row_count
	print("Percent of "+str(enrollment_year)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(enrollment_year)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail2.any():
	print(str(eyMin1)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail2)
	percent_FallTill_ConfFail = len(Falltill_fail2)/row_count
	print("Percent of "+str(eyMin1)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin1)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail3.any():
	print(str(eyMin2)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail3)
	percent_FallTill_ConfFail = len(Falltill_fail3)/row_count
	print("Percent of "+str(eyMin2)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin2)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail4.any():
	print(str(eyMin3)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail4)
	percent_FallTill_ConfFail = len(Falltill_fail4)/row_count
	print("Percent of "+str(eyMin3)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin3)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail5.any():
	print(str(eyMin4)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail5)
	percent_FallTill_ConfFail = len(Falltill_fail5)/row_count
	print("Percent of "+str(eyMin4)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin4)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail6.any():
	print(str(eyMin5)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail6)
	percent_FallTill_ConfFail = len(Falltill_fail6)/row_count
	print("Percent of "+str(eyMin5)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin5)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Falltill_fail7.any():
	print(str(eyMin6)+" Fields with Failed Fall Tillage Confidence Index:")
	print(Falltill_fail7)
	percent_FallTill_ConfFail = len(Falltill_fail7)/row_count
	print("Percent of "+str(eyMin6)+" Fields with Failed Fall Tillage Confidence Index: " +str(round(percent_FallTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin6)+" Fields Pass Fall Tillage Confidence Index")
	print("--------------------------------------------------------------------")


# Spring TIll check 

Springtill_fail1 = []
Springtill_fail2 = []
Springtill_fail3 = []
Springtill_fail4 = []
Springtill_fail5 = []
Springtill_fail6 = []
Springtill_fail7 = []
Springtill_fail1.append(dataEnrollment.loc[dataEnrollment['conf_index_spring_res'] <= 40, 'id'].values)
Springtill_fail2.append(dataEnrollmentMin1.loc[dataEnrollmentMin1['conf_index_spring_res'] <= 40, 'id'].values)
Springtill_fail3.append(dataEnrollmentMin2.loc[dataEnrollmentMin2['conf_index_spring_res'] <= 40, 'id'].values)
Springtill_fail4.append(dataEnrollmentMin3.loc[dataEnrollmentMin3['conf_index_spring_res'] <= 40, 'id'].values)
Springtill_fail5.append(dataEnrollmentMin4.loc[dataEnrollmentMin4['conf_index_spring_res'] <= 40, 'Id'].values)
Springtill_fail6.append(dataEnrollmentMin5.loc[dataEnrollmentMin5['conf_index_spring_res'] <= 40, 'Id'].values)
Springtill_fail7.append(dataEnrollmentMin6.loc[dataEnrollmentMin6['conf_index_spring_res'] <= 40, 'Id'].values)
Springtill_fail1 = unique(Springtill_fail1)
Springtill_fail2 = unique(Springtill_fail2)
Springtill_fail3 = unique(Springtill_fail3)
Springtill_fail4 = unique(Springtill_fail4)
Springtill_fail5 = unique(Springtill_fail5)
Springtill_fail6 = unique(Springtill_fail6)
Springtill_fail7 = unique(Springtill_fail7)


if Springtill_fail1.any():
	print(str(enrollment_year)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail1)
	percent_SpringTill_ConfFail = len(Springtill_fail1)/row_count
	print("Percent of "+str(enrollment_year)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(enrollment_year)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail2.any():
	print(str(eyMin1)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail2)
	percent_SpringTill_ConfFail = len(Springtill_fail2)/row_count
	print("Percent of "+str(eyMin1)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin1)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail3.any():
	print(str(eyMin2)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail3)
	percent_SpringTill_ConfFail = len(Springtill_fail3)/row_count
	print("Percent of "+str(eyMin2)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin2)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail4.any():
	print(str(eyMin3)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail4)
	percent_SpringTill_ConfFail = len(Springtill_fail4)/row_count
	print("Percent of "+str(eyMin3)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin3)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail5.any():
	print(str(eyMin4)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail5)
	percent_SpringTill_ConfFail = len(Springtill_fail5)/row_count
	print("Percent of "+str(eyMin4)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin4)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail6.any():
	print(str(eyMin5)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail6)
	percent_SpringTill_ConfFail = len(Springtill_fail6)/row_count
	print("Percent of "+str(eyMin5)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin5)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

if Springtill_fail7.any():
	print(str(eyMin6)+" Fields with Failed Spring Tillage Confidence Index:")
	print(Springtill_fail7)
	percent_SpringTill_ConfFail = len(Springtill_fail7)/row_count
	print("Percent of "+str(eyMin6)+" Fields with Failed Spring Tillage Confidence Index: " +str(round(percent_SpringTill_ConfFail *100, 2))+"%")
	print("--------------------------------------------------------------------")
else:
	print("All "+str(eyMin6)+" Fields Pass Spring Tillage Confidence Index")
	print("--------------------------------------------------------------------")

# TILLAGE 
projectTillStatus1 = "Passed"
projectTillStatus2 = "Passed"
projectPracticeStatus = "Passed"
projectCoverCropStatus = "Passed"

if percentFallTillNull >= 0.5:

	projectTillStatusNull = """

Failed

At least half of the fields are missing Fall Tillage data for the enrollment year. 
"""

elif percentSpringTillNull >= 0.5:

	projectTillStatusNull = """

Failed

At least half of the fields are missing Spring Tillage data for the enrollment year. 
"""

elif percentSpringTillNull >= 0.5 and percentFallTillNull >= 0.5:

	projectTillStatusNull = """

Failed

At least half of the fields are missing both Spring and Fall Tillage data for the enrollment year. 
"""

else:
	projectTillStatusNull = "Passed"

# check for tillage practice change eligibility. If they are doing tillage reduction,
# should not have feilds with conventional till in the practice change year. If confidence index >= 40 then the estimate is "reliable"

bad_till_year = ""

if dataEnrollment['practice_name'].str.contains('Tillage').any():
	# conventional tillage in enrollment year
	bad_fields_tillage.append(dataEnrollment.loc[(dataEnrollment['fall_till_class'] == 1) & (dataEnrollment['conf_index_fall_res'] >= 40), 'id'])
	bad_fields_tillage1.append(dataEnrollment.loc[(dataEnrollment['spring_till_class'] == 1) & (dataEnrollment['conf_index_spring_res'] >= 40), 'id'])
	bad_till_year = enrollment_year

	# check if no-till was tagged in the past 
	if LastCropYear == eyMin1:
		bad_fields_tillage2.append(dataEnrollmentMin1.loc[(dataEnrollmentMin1['fall_till_class'] == 3) & (dataEnrollmentMin1['conf_index_fall_res'] >= 40), 'id'])
		bad_fields_tillage3.append(dataEnrollmentMin1.loc[(dataEnrollmentMin1['spring_till_class'] == 3) & (dataEnrollmentMin1['conf_index_spring_res'] >= 40), 'id'])
		bad_till_year = eyMin1
	if LastCropYear == eyMin2:
		bad_fields_tillage2.append(dataEnrollmentMin2.loc[(dataEnrollmentMin2['fall_till_class'] == 3) & (dataEnrollmentMin2['conf_index_fall_res'] >= 40), 'id'])
		bad_fields_tillage3.append(dataEnrollmentMin2.loc[(dataEnrollmentMin2['spring_till_class'] == 3) & (dataEnrollmentMin2['conf_index_spring_res'] >= 40), 'id'])
		bad_till_year = eyMin2
	if LastCropYear == eyMin3:
		bad_fields_tillage2.append(dataEnrollmentMin3.loc[(dataEnrollmentMin3['fall_till_class'] == 3) & (dataEnrollmentMin3['conf_index_fall_res'] >= 40), 'id'])
		bad_fields_tillage3.append(dataEnrollmentMin3.loc[(dataEnrollmentMin3['spring_till_class'] == 3) & (dataEnrollmentMin3['conf_index_spring_res'] >= 40), 'id'])
		bad_till_year = eyMin3
	if LastCropYear == eyMin4:
		bad_fields_tillage2.append(dataEnrollmentMin4.loc[(dataEnrollmentMin4['fall_till_class'] == 3) & (dataEnrollmentMin4['conf_index_fall_res'] >= 40), 'Id'])
		bad_fields_tillage3.append(dataEnrollmentMin4.loc[(dataEnrollmentMin4['spring_till_class'] == 3) & (dataEnrollmentMin4['conf_index_spring_res'] >= 40), 'Id'])
		bad_till_year = eyMin4
	if LastCropYear == eyMin5:
		bad_fields_tillage2.append(dataEnrollmentMin5.loc[(dataEnrollmentMin5['fall_till_class'] == 3) & (dataEnrollmentMin5['conf_index_fall_res'] >= 40), 'Id'])
		bad_fields_tillage3.append(dataEnrollmentMin5.loc[(dataEnrollmentMin5['spring_till_class'] == 3) & (dataEnrollmentMin5['conf_index_spring_res'] >= 40), 'Id'])
		bad_till_year = eyMin5
	if LastCropYear == eyMin6:
		bad_fields_tillage2.append(dataEnrollmentMin6.loc[(dataEnrollmentMin6['fall_till_class'] == 3) & (dataEnrollmentMin6['conf_index_fall_res'] >= 40), 'Id'])
		bad_fields_tillage3.append(dataEnrollmentMin6.loc[(dataEnrollmentMin6['spring_till_class'] == 3) & (dataEnrollmentMin6['conf_index_spring_res'] >= 40), 'Id'])
		bad_till_year = eyMin6



print("OpTIS Tillage Eligibility: " + projectTillStatusNull)


for b in bad_fields_tillage:
	if b.empty == True:
		pass
	else:
		print("There are "+str(bad_till_year)+" fields with Fall conventional tillage flagged by OpTIS, but tillage reduction is assigned as a practice change.")
		percent_badFallTillFields = len(b)/row_count
		print("Fields with Fall Conventional Till Mismatch:")
		print(b.values)
		print("Percent of "+str(bad_till_year)+" Fields with Fall Till Mismatch: " +str(round(percent_badFallTillFields *100, 2))+"%")


for b in bad_fields_tillage1:
	if b.empty == True:
		pass
	else:
		print("")
		print("There are "+str(bad_till_year)+" fields with Spring conventional tillage flagged by OpTIS, but tillage reduction is assigned as a practice change.")
		percent_badSpringTillFields = len(b)/row_count
		print("Fields with Spring Conventional Till Mismatch")
		print(b.values)
		print("Percent of "+str(bad_till_year)+" Fields with Spring Till Mismatch: " +str(round(percent_badSpringTillFields *100, 2))+"%")


for b in bad_fields_tillage2:
	if b.empty == True:
		pass
	else:
		print("")
		print("There are "+str(bad_till_year)+" fields with Fall no-till flagged by OpTIS the last year this crop was grown, but tillage reduction is assigned as a practice change.")
		percent_badFallNoTillFields = len(b)/row_count
		print("Fields with Fall No-Till Mismatch")
		print(b.values)
		print("Percent of "+str(bad_till_year)+" Fields with Fall No-Till Mismatch: " +str(round(percent_badFallNoTillFields *100, 2))+"%")

for b in bad_fields_tillage3:
	if b.empty == True:
		pass
	else:
		print("")
		print("There are "+str(bad_till_year)+" fields with Spring no-till flagged by OpTIS the last year this crop was grown, but tillage reduction is assigned as a practice change.")
		percent_badSpringNoTillFields = len(b)/row_count
		print("Fields with Spring No-Till Mismatch")
		print(b.values)
		print("Percent of "+str(bad_till_year)+" Fields with Spring No-Till Mismatch: " +str(round(percent_badSpringNoTillFields *100, 2))+"%")


### END TILLAGE SECTION 
###################################
# PRACTICE CHANGE - Determine when last time commodity crop was grown 
print("""
------------------------------------------------------------------------------ 
""")

# if cover crop was practice change, but cover crop is shown the last year commodity was grown (and conficence > 0.7, flag field)
if LastCropYear == eyMin1:
	percentFallTillNull_Prac = NullFallTillMin1/row_count
	percentSpringTillNull_Prac = NullSpringTillMin1/row_count
	coverCropCountLastCropYear = dataEnrollmentMin1['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin1.loc[(dataEnrollmentMin1['cover_crop'] >= 1) & (dataEnrollmentMin1['conf_index_cover_crop'] >= 0.7), 'id'])
if LastCropYear == eyMin2:
	# tillage 
	percentFallTillNull_Prac = NullFallTillMin2/row_count
	percentSpringTillNull_Prac = NullSpringTillMin2/row_count
	# cover cropping
	coverCropCountLastCropYear = dataEnrollmentMin2['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin2.loc[(dataEnrollmentMin2['cover_crop'] >= 1) & (dataEnrollmentMin2['conf_index_cover_crop'] >= 0.7), 'id'])
if LastCropYear == eyMin3:
	percentFallTillNull_Prac = NullFallTillMin3/row_count
	percentSpringTillNull_Prac = NullSpringTillMin3/row_count
	coverCropCountLastCropYear = dataEnrollmentMin3['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin3.loc[(dataEnrollmentMin3['cover_crop'] >= 1) & (dataEnrollmentMin3['conf_index_cover_crop'] >= 0.7), 'id'])

if LastCropYear == eyMin4:
	coverCropCountLastCropYear = dataEnrollmentMin4['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin4.loc[(dataEnrollmentMin4['cover_crop'] >= 1) & (dataEnrollmentMin4['conf_index_cover_crop'] >= 0.7), 'Id'])
if LastCropYear == eyMin5:
	coverCropCountLastCropYear = dataEnrollmentMin5['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin5.loc[(dataEnrollmentMin5['cover_crop'] >= 1) & (dataEnrollmentMin5['conf_index_cover_crop'] >= 0.7), 'Id'])
if LastCropYear == eyMin6:
	coverCropCountLastCropYear = dataEnrollmentMin6['cover_crop'].sum()
	bad_fields_cc.append(dataEnrollmentMin6.loc[(dataEnrollmentMin6['cover_crop'] >= 1) & (dataEnrollmentMin6['conf_index_cover_crop'] >= 0.7), 'Id'])


# cover crop eligibility check 
if dataEnrollment['practice_name'].str.contains('Cover').any():
	#print(coverCropCountLastCropYear)
	try:
		if coverCropCountLastCropYear >= 1:
			projectCoverCropStatus = """

Failed

In the last year this crop was grown, OpTis flagged cover crop or winter commodity occurrence. 
However, Cover Cropping is listed as a practice change.
	"""
		else:
			projectCoverCropStatus = "Passed"
	except:
		projectCoverCropStatus = "Passed"


if percentCCNull >= 0.5:

	projectCCStatusNull = """

Failed

At least half of the fields are missing cover crop data for the enrollment year. 
"""
else:
	projectCCStatusNull = ""

print("OpTIS Cover Cropping Eligibility: " + projectCoverCropStatus+projectCCStatusNull)

for b in bad_fields_cc:
	if b.empty == True:
		pass
	else:
		percent_badCCFields = len(b)/row_count
		print("Fields with cover crop mismatch")
		print(b.values)
		print("Percent of "+str(LastCropYear)+" Fields with Cover Crop Mismatch: " +str(round(percent_badCCFields *100, 2))+"%")
print("""
------------------------------------------------------------------------------ 
""")

# Written by Austin Arrington. Copyright 2022 ESMC
