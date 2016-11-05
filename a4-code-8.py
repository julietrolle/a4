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

grouped_by_patient = current[['PatientID', 'Visit', 'Dilution', 'Betatoxin']].groupby("PatientID")

for _, patient_df in grouped_by_patient:
    grouped_by_visit = patient_df.groupby('Visit')

    series = [visit_df[["Dilution", "Betatoxin"]] for _, visit_df in grouped_by_visit]
    series[0]
    plt.plot(series[0]["Dilution"], series[0]["Betatoxin"])
    plt.ylabel('Intensity')
    plt.xlabel('Dilution')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    if len(series)==2:
        series[0]
        series[1]
        plt.plot(series[0]["Dilution"], series[0]["Betatoxin"])
        plt.plot(series[1]["Dilution"], series[1]["Betatoxin"])
        plt.ylabel('Intensity')
        plt.xlabel('Dilution')
        plt.title('Dilution vs Intensity, Betatoxin')
        plt.xscale('log')
        plt.yscale('log')
        plt.show
    if len(series)== 3:
        series[0]
        series[1]
        series[2]
        plt.plot(series[0]["Dilution"], series[0]["Betatoxin"])
        plt.plot(series[1]["Dilution"], series[1]["Betatoxin"])
        plt.plot(series[2]["Dilution"], series[2]["Betatoxin"])
        plt.ylabel('Intensity')
        plt.xlabel('Dilution')
        plt.title('Dilution vs Intensity, Betatoxin')
        plt.xscale('log')
        plt.yscale('log')
        plt.show