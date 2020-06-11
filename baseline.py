import pandas as pd
import numpy as np
from operator import itemgetter
import easygui
from datetime import datetime

#choose file
path = easygui.fileopenbox()
#read excel to dataframe
data = pd.read_excel(path, sheet_name = 'Mapped AD IMS for testing-new', usecols = ['Milestone', 'ACIO', 'Application', 'Start_Date_(Before_CPDs)', 'Baseline_Start', 'Status_Date', 'PercentComp', 'Release1', 'GANTT RELEASE'])
date = (data.at[1,'Status_Date']).strftime("%d_%b_%Y")
#remove unnecessary data from the dataframe
rowIndex = []
for index, row in data.iterrows():
	if row['Milestone'] == 'RELEASE' and row['ACIO'][0:2] == 'AD' and row['PercentComp'] != 1.0:
		rowIndex.append(index)
	elif row['Milestone'] == 'INITIATIVE' and row['ACIO'][0:2] != 'AD':
		rowIndex.append(index)
	if row['Milestone'] == 'APPLICATION' and row['ACIO'][0:2] != 'AD':
		rowIndex.append(index)
data = data.iloc[rowIndex]
#Build dataframes
#Create 2 lists
baseline = []
late = []
now = datetime.now()
#Add data to correct lists
for index, row in data.iterrows():
	base = row['Baseline_Start']
	start = row['Start_Date_(Before_CPDs)']
	days = (now - start).days
	if pd.isnull(base) and (days > 60):
		if row['Milestone'] == 'RELEASE':
			baseline.append((row['ACIO'], row['Application'], row['Release1'], row['GANTT RELEASE'], days))
		else:
			baseline.append((row['ACIO'], row['Application'], float('NaN'), float('NaN'), days))

for index, row in data.iterrows():
	base = row['Baseline_Start']
	start = row['Start_Date_(Before_CPDs)']
	if not pd.isnull(base) and (base - start).days > 0:
		late.append((row['ACIO'], row['Application'], (base - start).days))


#convert to dataframes
baseline = pd.DataFrame(sorted(sorted(baseline,key=itemgetter(1)), key=itemgetter(0)), columns = ['ACIO', 'Application', 'Release', 'Gant Release', 'Days Past Start Date'])
late = pd.DataFrame(sorted(sorted(late,key=itemgetter(1)), key=itemgetter(0)), columns = ['ACIO', 'Application', 'Days Past Baseline'])

#write to excel
with pd.ExcelWriter('BaselineComparison_'+ date + '.xlsx') as writer:  
	baseline.to_excel(writer, sheet_name = 'No Baseline',index = False)
	late.to_excel(writer, sheet_name = 'Late Start',index = False)

print('Finished')