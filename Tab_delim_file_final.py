import pandas as pd
import pprint
import numpy as np

def splitSampleID(sampleID):
    temp = sampleID.split()
    if len(temp) == 3:
        return {'patientID': temp[0], 'visit': temp[1], 'dilution': temp[2]}
    elif len(temp) == 1:
        return {'patientID':temp[0]}
    elif len(temp) == 2:
        if temp[1].isdigit():
            return {'patientID': temp[0], 'dilution': temp[1]}
        else:
            s = temp[1]
            found_one = False
            dilution = visit = ''
            for i in range(0, len(s)):
                letter = s[len(s) - i - 1]
                if (not found_one):
                    dilution = letter + dilution
                    if (letter == '1'):
                        found_one = True
                    return {'patientID': temp[0], 'dilution': temp[1]}
                else:
                    #visit = letter + visit
                    return {'patientID': temp[0], 'visit': letter + visit}
        #return {'patientID': temp[0]}
    else:
        return {'patientID':' '.join(temp[0:-2]), 'visit' : temp[-2], 'dilution' : temp[-1]}

def new_cols(spl_dict, dfr): #inserts parsed patientIDs into new columns in dataframe
    for idx, d in spl_dict.items():
        dfr.ix[idx, 'PatientID'] = d['patientID']
        if 'visit' in d:
            dfr.ix[idx, 'Visit'] = d['visit']
        else:
            pass
        if 'dilution' in d:
            dfr.ix[idx, 'Dilution'] = d['dilution']
        else:
            pass

def find_unique_patientID(dfr):
    test = list(dfr['PatientID'].unique())
    return test

def implied_hosp_fn(hosp_dict, dfr): #to insert implied hospital values into all rows of the col
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

d = 1.0
e = int(d)
f = 'somestring'

df = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname=None, header=1)  # makes a dictionary of sheets to parse through all sheets in xl file
# print (df)

for sheetname in df:
    current = df[sheetname] # allows us to figure stuff out for one plate before we do it for all

    split_dict = {}
    for row in current.iterrows():
        #print(list(row[1].iteritems()))
        split_dict[row[0]] = splitSampleID(row[1][0])
    #pprint.pprint(split_dict)

    new_cols(split_dict, current)
    print(current[['PatientID', 'Visit', 'Dilution']])

    unique_patientID_list = find_unique_patientID(current)
    #print(unique_patientID_list)

    #for tab-delimited dataframe

    hospital_dict = {}
    for row in current.iterrows():
        hospital_dict[row[0]] = row[1][1]
    #pprint.pprint(hospital_dict)

    gender_dict = {}
    for row in current.iterrows():
        gender_dict[row[0]] = row[1][3]
    #pprint.pprint(gender_dict)

    current1 = current.replace(np.nan, 'placeholder', regex=True) #to replace nan in dict with placeholder

    age_dict = {}
    for row in current1.iterrows():
        age_dict[row[0]] = row[1][2]
    #pprint.pprint(age_dict)

    implied_hosp_fn(hospital_dict, current)
    implied_gend_fn(gender_dict, current)
    implied_ag_fn(age_dict, current)

    print(current)

    current.to_csv('current_output%s.csv' % sheetname, sep='\t') #creates csv file with dataframe

