import pandas as pd
import pprint

df = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname=None, header=1)  # makes a dictionary of sheets to parse through all sheets in xl file
# print (df)

current = df['Plate 1'] # allows us to figure stuff out for one plate before we do it for all

    #my original code
# current['SampleID'] = current['Sample ID']
# print(current)
# print(current['Sample ID'])
#print(current['SampleID'])
# plots = ['surface protein ext','cytoplasmic ext', ...]
# current['PatientID'] = current.apply(lambda x: x.SampleID.split()[0:-2], axis=1)
# current['Replicate'] = current.apply(lambda x: x.SampleID.split()[-2], axis=1) #problems in plates 3-6, add if statement if 'V' in string? or create placeholder for values not found
# current['Dilution'] = current.apply(lambda x: x.SampleID.split()[-1], axis=1)

#print(current[['PatientID', 'Replicate', 'Dilution']])

    #after chatting with Mark:
def splitSampleID(sampleID):
    #print(sampleID)
    temp = sampleID.split()
    if len(temp) == 3:
        return {'patientID': temp[0], 'visit': temp[1], 'dilution': temp[2]}
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
print(current[['PatientID', 'Visit', 'Dilution']])

def find_unique_patientID(dfr):
    test = list(dfr['PatientID'].unique())
    return test

unique_patientID_list = find_unique_patientID(current)
print(unique_patientID_list)

# print(current.groupby('PatientID').groups)

def groupby_fn(dfr, patient):
    return dfr.ix[dfr['PatientID'] == patient, :]

for patient in unique_patientID_list:
    groupby_fn(current, patient) #print this to see what it does
    #input plotting code

