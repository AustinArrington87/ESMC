import csv
import pandas as pd
import numpy as np



project_years = [2021, 2020, 2019, 2018]

# Load Data
file1 = 'mrv_data.csv'
file2 = 'optis_data.csv'
project_name = "Benson_Hill"

def unique(list1):
	x = np.array(list1)
	return(np.unique(x))

def MergeDataByYear (season, project, mrv_file, opt_file):

	df_mrv = pd.read_csv(mrv_file, usecols = ['project_name', 'producer_name', 'id', 'field_name', 
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

	# projects 
	projects = df_mrv['project_name']
	project_list = projects.to_list()
	project_list_unique = unique(project_list)
	print(project_list_unique)

	# isolate Benson Hills MRV project 
	if project == "Benson_Hill":
		mrv_projName = "Benson Hill"
		opt_projName = "Benson Hill 2021 Fields"

	MRVprojectFrame = df_mrv.loc[df_mrv['project_name'] == mrv_projName]
	MRVprojFrameByYear = MRVprojectFrame[MRVprojectFrame['season'] == season]
	OPTprojectFrame = df_opt.loc[df_opt['source'] == opt_projName]
	OPTprojFrameByYear = OPTprojectFrame[OPTprojectFrame['year'] == season]

	print(MRVprojFrameByYear)
	print(OPTprojFrameByYear)

	MRV_Opt_Merged = MRVprojFrameByYear.merge(OPTprojFrameByYear, left_on="id", right_on='Id')[['project_name', 'producer_name', 'id', 'field_name', 
	'initial_year', 'year', 'practice_name', 'crop_name', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name']]

	MRV_Opt_Merged.to_csv(project+'_Merged_'+str(season)+'.csv', encoding='utf-8')


# call function 

for year in project_years:
	MergeDataByYear(year, project_name, file1, file2)


# Copyright 2022 ESMC
