import csv
import pandas as pd
import numpy as np

def unique(list1):
	x = np.array(list1)
	return(np.unique(x))

# define data frames from MRV and OpTIS
df_mrv = pd.read_csv('mrv_data.csv', usecols = ['project_name', 'producer_name', 'id', 'field_name', 
	'initial_year', 'season', 'practice_name', 'crop_name'])
df_opt = pd.read_csv('optis_data.csv', usecols = ['Name', 'Id', 'year', 'cover_crop', 'conf_index_cover_crop', 
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

# isolate Benson Hills project 
Benson_Hill = df_mrv.loc[df_mrv['project_name'] == 'Benson Hill']
print(Benson_Hill)
# only look at rows where there is not a NULL in practice_name
Benson_Hill_prac = Benson_Hill[Benson_Hill['practice_name'] != '[NULL]']
print(Benson_Hill_prac)


##### OpTIS Data #####
print(df_opt)


















