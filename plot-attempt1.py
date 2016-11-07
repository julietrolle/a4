% matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import numpy as np

df= pd.read_excel('06222016 Staph Array Data.xlsx',sheetname=None, header=1)
current= df['Plate 1']
def splitSampleID(sampleID):
    temp = sampleID.split()
    if len(temp) == 3:
        return {'patientID': temp[0], 'visit': temp[1], 'dilution': temp[2]}
    else:
        return {'patientID': temp[0], 'visit': "Not_found", 'dilution': temp[1]}

split_dict = {}
for row in current.iterrows():
    split_dict[row[0]] = splitSampleID(row[1][0])

def new_cols(spl_dict):
    for idx, d in spl_dict.items():
        current.ix[idx, 'PatientID'] = d['patientID']
        current.ix[idx, 'Visit'] = d['visit']
        current.ix[idx, 'Dilution'] = d['dilution']

new_cols(split_dict)

for i, group in current.groupby('PatientID'):
    plt.figure()
    group.plot(x='Dilution', y= 'Betatoxin', title=str(i))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Intensity')