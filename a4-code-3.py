import pandas as pd
import pprint
import numpy as np

df = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname=None, header=1)  # makes a dictionary of sheets to parse through all sheets in xl file
# print (df)

current = df['Plate 1'] # allows us to figure stuff out for one plate before we do it for all

    #after chatting with Mark:
def splitSampleID(sampleID):
    #print(sampleID)
    temp = sampleID.split()
    if len(temp) == 3:
        return {'patientID': temp[0], 'visit': temp[1], 'dilution': temp[2]}
    elif len(temp)== 2:
        return {'patientID': temp[0], 'visit': "Not_found", 'dilution': temp[1]}
    else:
        return {'patientID': temp[0], 'visit': "Not_found", 'dilution': temp[1]}

# {rowid: {'patientID': asd, 'visit':v1, 'dilution':1231}, }
split_dict = {}
for row in current.iterrows():
    #print(list(row[1].iteritems()))
    split_dict[row[0]] = splitSampleID(row[1][0])

#pprint.pprint(split_dict)

def new_cols(spl_dict, dfr):     #to take the split data and put it into the current dataframe in new columns
    for idx, d in spl_dict.items():
        dfr.ix[idx, 'PatientID'] = d['patientID']
        dfr.ix[idx, 'Visit'] = d['visit']
        dfr.ix[idx, 'Dilution'] = d['dilution']
    return dfr

new_cols(split_dict, current)
#print(current[['PatientID', 'Visit', 'Dilution']])

def find_unique_patientID(dfr):
    test = list(dfr['PatientID'].unique())
    return test

unique_patientID_list = find_unique_patientID(current)
#print(unique_patientID_list)

# print(current.groupby('PatientID').groups)

# def groupby_fn(dfr, patient):
#     return dfr.ix[dfr['PatientID'] == patient, :]
#
# for patient in unique_patientID_list:
#     (groupby_fn(current, patient)) #print this to see what it does

#for tab-delimited dataframe
hospital_dict = {}
for row in current.iterrows():
    hospital_dict[row[0]] = row[1][1]

# pprint.pprint(hospital_dict)

gender_dict = {}
for row in current.iterrows():
    gender_dict[row[0]] = row[1][3]

# pprint.pprint(gender_dict)

current1 = current.replace(np.nan, 'placeholder', regex=True) #to replace nan in dict with placeholder

age_dict = {}
for row in current1.iterrows():
    age_dict[row[0]] = row[1][2]

#pprint.pprint(age_dict)

d = 1.0
e = int(d)
f = 'somestring'

def implied_hosp_fn(hosp_dict, dfr):
    hosp_float_list = []
    for idx, hosp in hosp_dict.items():
        if type(hosp) == type(d):
            hosp = str(hosp)
            hosp_float_list.append(idx)
        if (idx) not in hosp_float_list:
            dfr.ix[idx, 'Hospital '] = str(hosp_dict[idx])
        if (idx - 1) not in hosp_float_list:
            if idx >= 1:
                dfr.ix[idx, 'Hospital '] = str(hosp_dict[(idx - 1)])
        if (idx - 2) not in hosp_float_list:
            if idx >= 2:
                dfr.ix[idx, 'Hospital '] = str(hosp_dict[(idx - 2)])
        if (idx - 3) not in hosp_float_list:
            if idx >= 3:
                dfr.ix[idx, 'Hospital '] = str(hosp_dict[(idx - 3)])
    return dfr

def implied_gend_fn(gend_dict, dfr):
    gend_float_list = []
    for idx, gend in gend_dict.items():
        if type(gend) == type(d):
            gend = str(gend)
            gend_float_list.append(idx)
        if (idx) not in gend_float_list:
            dfr.ix[idx, 'Gender'] = str(gend_dict[idx])
        if (idx - 1) not in gend_float_list:
            if idx >= 1:
                dfr.ix[idx, 'Gender'] = str(gend_dict[(idx - 1)])
        if (idx - 2) not in gend_float_list:
            if idx >= 2:
                dfr.ix[idx, 'Gender'] = str(gend_dict[(idx - 2)])
        if (idx - 3) not in gend_float_list:
            if idx >= 3:
                dfr.ix[idx, 'Gender'] = str(gend_dict[(idx - 3)])
    return dfr

def implied_ag_fn(ag_dict, dfr):
    ag_float_list = []
    for idx, ag in ag_dict.items():
        if type(ag) != type(f):
            ag_float_list.append(idx)
        if (idx) in ag_float_list:
            dfr.ix[idx, 'Age'] = ag_dict[idx]
        if (idx - 1) in ag_float_list:
            if idx >= 1:
                dfr.ix[idx, 'Age'] = ag_dict[(idx - 1)]
        if (idx - 2) in ag_float_list:
            if idx >= 2:
                dfr.ix[idx, 'Age'] = ag_dict[(idx - 2)]
        if (idx - 3) in ag_float_list:
            if idx >= 3:
                dfr.ix[idx, 'Age'] = ag_dict[(idx - 3)]
    #print(ag_float_list)
    return dfr

implied_hosp_fn(hospital_dict, current)
implied_gend_fn(gender_dict, current)
implied_ag_fn(age_dict, current)

print(current)

current.to_csv('current_output.csv', sep='\t') #creates csv file with dataframe