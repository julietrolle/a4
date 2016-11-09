import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pprint
import numpy as np
import math

def splitSampleID(sampleID): #parses through all plates and produces a dict for each
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
                    return {'patientID': temp[0], 'visit': letter + visit}
    else:
        return {'patientID':' '.join(temp[0:-2]), 'visit' : temp[-2], 'dilution' : temp[-1]}

def new_cols(spl_dict, dfr): #puts parsed info in new colums in the dataframe
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

def find_unique_patientID(dfr): #makes lists for each unique patient
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

def implied_gend_fn(gend_dict, dfr): #to insert implied gender values into all rows of the col
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

def implied_ag_fn(ag_dict, dfr): #to insert implied age values into all rows of the col
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

d = 1.0 #for datatype comparisons - needed for implied values functions
e = int(d)
f = 'somestring'

df= pd.read_excel('06222016 Staph Array Data.xlsx',sheetname=None, header=1)

for sheetname in df: #to loop over all sheets of the excel file
    current= df[sheetname]
    to_drop = ['Standard1', 'Standard2', 'Standard3', 'Standard4', 'Standard5', 'Standard6', 'Standard 7']
    current = current[~current['Sample ID'].str.contains('|'.join(to_drop), na=False, regex=False)] #to remove standards

    split_dict = {}
    for row in current.iterrows():
        split_dict[row[0]] = splitSampleID(row[1][0])

    new_cols(split_dict, current)

    treatments = [ "PSMalpha2", "PSMalpha3","psmalpah4", "Betatoxin","hIgA", "LDL","SEB","S.Pyogenese arcA",
                 "LukE","Pn PS12","LukD","Pn PS23","HLA-1","SpA domD5-WT","Glom.extract","SpA domD5FcNull","SEN",
                 "hIgG","SEU","HLA","SEI","LukAB(Lab)","SEM","LukAB(cc30)","surface protein ext","SEB",
                 "cytoplasmic ext","Hemolysin gamma A","Pn CWPS","Hemolysin gamma B","ABA","Hemolysin gamma C",
                 "PC-12","LukS-PV","SEO","SP","SEG","PLY","HSA","Exoprotein ext","Rabbit IgG","LukF-PV",
                 "PSM 4variant","PC4","PNAG","PC16","HLA -2","Tetanus Toxoid",]

    grouped_by_patient = current[['PatientID', 'Visit', 'Dilution'] + treatments].groupby("PatientID")

    matplotlib.rcParams.update({'font.size': 10})

    with PdfPages('a4_output%s2nd.pdf' % sheetname) as pdf: #makes plots
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

    #generates tab delimited dataframe with implied values filled in
    split_dict = {}
    for row in current.iterrows():
        # print(list(row[1].iteritems()))
        split_dict[row[0]] = splitSampleID(row[1][0])
    # pprint.pprint(split_dict)

    new_cols(split_dict, current)
    print(current[['PatientID', 'Visit', 'Dilution']])

    unique_patientID_list = find_unique_patientID(current)
    # print(unique_patientID_list)

    hospital_dict = {}
    for row in current.iterrows():
        hospital_dict[row[0]] = row[1][1]
    # pprint.pprint(hospital_dict)

    gender_dict = {}
    for row in current.iterrows():
        gender_dict[row[0]] = row[1][3]
    # pprint.pprint(gender_dict)

    current1 = current.replace(np.nan, 'placeholder', regex=True)  # to replace nan in dict with placeholder

    age_dict = {}
    for row in current1.iterrows():
        age_dict[row[0]] = row[1][2]
    # pprint.pprint(age_dict)

    implied_hosp_fn(hospital_dict, current)
    implied_gend_fn(gender_dict, current)
    implied_ag_fn(age_dict, current)

    print(current)

    current.to_csv('current_output%s.csv' % sheetname, sep='\t')  # creates csv file with dataframe