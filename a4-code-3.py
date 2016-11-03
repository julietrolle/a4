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

def new_cols(spl_dict):
    for idx, d in spl_dict.items():
        current.ix[idx, 'PatientID'] = d['patientID']
        current.ix[idx, 'Visit'] = d['visit']
        current.ix[idx, 'Dilution'] = d['dilution']

new_cols(split_dict)
print(current[['PatientID', 'Visit', 'Dilution']])
