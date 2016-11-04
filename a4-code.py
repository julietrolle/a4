import pandas as pd
#import matplotlib
#import numpy as np
#import matplotlib.pyplot as plt
import xlrd

#matplotlib.style.use('ggplot')
#import pprint

df = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname=None, header=1) #makes a dictionary of sheets to parse through all sheets in xl file
#print (df)
for sheetname in df:
    sheet = df[sheetname] #creating sheet to parse thru
    for values in sheet.values:
        unparsed = values[0]
        parsed_list = unparsed.split()      #splitting on whitespace to get patient info since data is not all written the same
        #print(len(parsed_list))
        parsed_list_len = len(parsed_list)

        patient = None      #setting variables for information needed
        visit = None
        dilution = None
#creating decision tree to parse through the data for patient information
        if parsed_list_len == 1:            #if 1 just patient info
            patient = parsed_list[0]
        elif parsed_list_len == 2:          #if two first string is patient, second is dilution
            if parsed_list[1].isdigit():
                patient = parsed_list[0]
                dilution = parsed_list[1]
            else:
                s = parsed_list[1]
                found_one = False
                dilution = visit = ''
                for i in range(0, len(s)):
                    letter = s[len(s) - i - 1]
                    if (not found_one):
                        dilution = letter + dilution
                        if (letter == '1'):
                            found_one = True
                        else:
                            visit = letter + visit
                #print(patient, visit, dilution)
        elif parsed_list_len == 3:                  #if three first string is patient second is visit third is dilution
            patient = parsed_list[0]
            visit = parsed_list[1]
            dilution = parsed_list[2]
            #print (patient, visit, dilution)
        else:
            patient = ''.join(parsed_list[0:-2])
            visit = parsed_list[-2]
            dilution = parsed_list[-1]
            #print(patient, visit, dilution)

        #print (patient, visit, dilution)

#print (list(df['Plate 1']['Betatoxin'].items()))
#c = df['Plate 1']['Betatoxin'].items()

print(df['Plate 1']['Sample ID'])
#print(df['Plate 1']['Betatoxin'].items())
#d = list(c)
#x = []
#for tuple in d:
 #   x.append(tuple[0])
#print (x)
#y = []
#for tuple in d:
 #   y.append(tuple[1])
#print(y)