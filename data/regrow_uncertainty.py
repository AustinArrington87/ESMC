import json
import numpy as np


# load JSON file 
loadData = open("benson_hill_dndc_results.json", 'r')
dicData = json.loads(loadData.read())
#print(dicData)
data = dicData['data']['session_uncertainties']
#print(data)
BH_Field_1 = data['BH-Field-1_2021']
BH_Field_2 = data['BH-Field-2_2021']
BH_Field_3 = data['BH-Field-3_2021']
BH_Field_4 = data['BH-Field-4_2021']
Field_List = [BH_Field_1, BH_Field_2, BH_Field_3, BH_Field_4]

def calcUncertainty (field):
	baseline = field['scenarios_uncertainties']['baseline']
	practice = field['scenarios_uncertainties']['practice_change']

	############### BASELINE #######
	# baseline - SOC
	b_dSOC = baseline['dsoc']
	b_dSOC_uncertainty = b_dSOC['distribution']
	b_dSOC_uncertainty = round(np.percentile(b_dSOC_uncertainty, 52.5),4)
	b_dSOC_std = round(b_dSOC['standard_deviation'],4)
	# baseline direct n2o
	b_N2O = baseline['direct_n2o']
	b_N2O_uncertainty= b_N2O['distribution']
	b_N2O_uncertainty = round(np.percentile(b_N2O_uncertainty, 47.5),4)
	b_N2O_std = round(b_N2O['standard_deviation'],4)
	# baseline indirect n2o
	b_indirectN2O = baseline['indirect_n2o']
	# baseline ch4
	b_ch4 = baseline['ch4']
	#########PRACTICE#########
	# practice - SOC
	p_dSOC = practice['dsoc']
	p_dSOC_uncertainty = p_dSOC['distribution']
	p_dSOC_uncertainty = round(np.percentile(p_dSOC_uncertainty, 47.5),4)
	p_dSOC_std = round(p_dSOC['standard_deviation'],4)
	# practice - direct n2o
	p_N2O = practice['direct_n2o']
	p_N2O_uncertainty= p_N2O['distribution']
	p_N2O_uncertainty = round(np.percentile(p_N2O_uncertainty, 52.5),4)
	p_N2O_std = round(p_N2O['standard_deviation'],4)
	# practice indirect n2o
	p_indirectN2O = practice['indirect_n2o']
	# practice ch4
	p_ch4 = practice['ch4']

	return {
		"field": field['name'],
		"dSOC": {
		"baseline": b_dSOC_uncertainty,
		"practice": p_dSOC_uncertainty
		},
		"dSOC_std": {
		"baseline": b_dSOC_std,
		"practice": p_dSOC_std
		},
		"n2o_direct": {
		"baseline": b_N2O_uncertainty,
		"practice": p_N2O_uncertainty
		},
		"n2o_direct_std": {
		"baseline": b_N2O_std,
		"practice": p_N2O_std
		},
		"n2o_indirect": {
		"baseline": b_indirectN2O,
		"practice": p_indirectN2O
		},
		"ch4": {
		"baseline": b_ch4,
		"practice": p_ch4
		}
	}

for f in Field_List:
	print(calcUncertainty(f))
