import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pprint
import numpy as np
import math

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

treatments = [ "PSMalpha2", "PSMalpha3","psmalpah4", "Betatoxin","hIgA", "LDL","SEB","S.Pyogenese arcA",
             "LukE","Pn PS12","LukD","Pn PS23","HLA-1","SpA domD5-WT","Glom.extract","SpA domD5FcNull","SEN",
             "hIgG","SEU","HLA","SEI","LukAB(Lab)","SEM","LukAB(cc30)","surface protein ext","SEB",
             "cytoplasmic ext","Hemolysin gamma A","Pn CWPS","Hemolysin gamma B","ABA","Hemolysin gamma C",
             "PC-12","LukS-PV","SEO","SP","SEG","PLY","HSA","Exoprotein ext","Rabbit IgG","LukF-PV",
             "PSM 4variant","PC4","PNAG","PC16","HLA -2","Tetanus Toxoid",]

grouped_by_patient = current[['PatientID', 'Visit', 'Dilution'] + treatments].groupby("PatientID")

matplotlib.rcParams.update({'font.size': 10})

with PdfPages('a4_output2.pdf') as pdf:
    for treatment in treatments:
        plt.suptitle(treatment)
        plot_count = 0

        for patient_id, patient_df in grouped_by_patient:
            plot_count += 1
            grouped_by_visit = patient_df.groupby('Visit')

            series = [visit_df[["Dilution", treatment]] for _, visit_df in grouped_by_visit]
            plt.subplot(2, math.ceil(float(len(grouped_by_patient)) / 2), plot_count)

            for s in series:
                plt.plot(s["Dilution"], s[treatment])
            plt.ylabel('Intensity')
            plt.xlabel('Dilution')
            plt.title('{0}'.format(patient_id), fontsize=10)
            plt.xscale('log')
            plt.yscale('log')

        plt.tight_layout(pad=2.5)
        pdf.savefig()
        plt.close()