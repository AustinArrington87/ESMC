import csv
import pandas as pd
import numpy as np

def unique(list1):
	x = np.array(list1)
	return(np.unique(x))

# define data frames from MRV and OpTIS
df_mrv = pd.read_csv('mrv_data.csv', usecols = ['project_name', 'producer_name', 'id', 'field_name', 
	'initial_year', 'season', 'practice_name', 'crop_name'])
df_opt = pd.read_csv('optis_data.csv', usecols = ['Name', 'Id', 'source', 'year', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name'])

#pd.options.display.max_rows = 9999
print(df_mrv)
#print(df_mrv.to_string())

# what crops are we workign with 
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

### Isolate a project --> Benson Hills 

# isolate Benson Hills MRV project 
Benson_Hill = df_mrv.loc[df_mrv['project_name'] == 'Benson Hill']
#print(Benson_Hill)
# only look at rows where there is not a NULL in practice_name
Benson_Hill_prac = Benson_Hill[Benson_Hill['practice_name'] != '[NULL]']
#print(Benson_Hill_prac)
# now isolate frame by year 
Benson_Hill_2021 = Benson_Hill_prac[Benson_Hill_prac['season'] == 2021]
print(Benson_Hill_2021)


##### OpTIS Data #####
#print(df_opt)
Benson_Hill_Optis = df_opt.loc[df_opt['source'] == 'Benson Hill 2021 Fields']
#print(Benson_Hill_Optis)
# isolate frame by year
Benson_Hill_Optis_2021 = Benson_Hill_Optis[Benson_Hill_Optis['year'] == 2021]
print(Benson_Hill_Optis_2021)

# check ids 
#df_new[df_new['l_ext'].isin([31, 22, 30, 25, 64])]

#df1.merge(df2, left_on='objectdesc', right_on='objdescription')[['Content', 'objectdesc', 'TS_id', 'idname']]
#Benson_Hill_prac.merge(Benson_Hill_Optis, left_on="id", right_on='Id')[['project_name', 'producer_name', 'id', 'field_name', 'season', 'practice_name', 'crop_name']]

BH_2021_Merged = Benson_Hill_2021.merge(Benson_Hill_Optis_2021, left_on="id", right_on='Id')[['project_name', 'producer_name', 'id', 'field_name', 
	'initial_year', 'season', 'practice_name', 'crop_name', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name']]

print(BH_2021_Merged)
# export DataFrame to CSV
#BH_2021_Merged.to_csv('BH_2021_Merged.csv', encoding='utf-8')

# Export CSV of all years (2021-2015), Merging MRV and OpTIS data for Benson Hills project 
BH_AllYears_Merged = Benson_Hill_prac.merge(Benson_Hill_Optis, left_on="id", right_on='Id')[['project_name', 'producer_name', 'id', 'field_name', 
	'initial_year', 'season', 'practice_name', 'crop_name', 'cover_crop', 'conf_index_cover_crop', 
	'fall_till_class', 'conf_index_fall_res', 'spring_till_class', 'conf_index_spring_res', 'name']]
print(BH_AllYears_Merged)
BH_AllYears_Merged.to_csv('BH_AllYears_Merged.csv', encoding='utf-8')

# Author: Austin Arrington
# Copyright Ecosystem Services Market Consoritum (ESMC) 2022 









