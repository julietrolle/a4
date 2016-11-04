import pandas as pd



dfs = pd.read_excel("06222016 Staph Array Data.xlsx", sheetname=None, header=1)
for sheetname in dfs:
    sheet = dfs[sheetname]
    patient = None
    visit = None
    dilution = None
    split_dict = {}
    for idx, val in enumerate(sheet.values):
        unparsed = val[0]
        parsed_list = unparsed.split()
        parsed_list_len = len(parsed_list)
        if parsed_list_len == 1:
            patient = parsed_list[0]
        elif parsed_list_len == 2:
            patient = parsed_list[0]
            if parsed_list[1].isdigit():
                dilution = parsed_list[1]
            else:
                s = parsed_list[1]
                found_one = False
                dilution = visit = ''
                for i in range(0, len(s)):
                    letter = s[len(s) - i - 1]
                    if (not found_one):
                        dilution = letter + dilution
                        if (letter == '1') :
                            found_one = True
                    else:
                        visit = letter + visit

        elif parsed_list_len == 3:
            patient = parsed_list[0]
            visit = parsed_list[1]
            dilution = parsed_list[2]
        else:
            patient = ' '.join(parsed_list[0:-2])
            visit = parsed_list[-2]
            dilution = parsed_list[-1]
        sheet.ix[idx, 'PatientID'] = patient
        sheet.ix[idx, 'Visit'] = visit
        sheet.ix[idx, 'Dilution'] = dilution

    for key, grp in sheet.groupby(['PatientID']):
            print (key, grp)
