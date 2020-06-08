import pandas as pd
import numpy as np
from operator import itemgetter
import easygui
from datetime import datetime

#choose file
path = easygui.fileopenbox()
#read excel to dataframe
data = pd.read_excel(path, sheet_name = 'Mapped AD IMS for testing-new', usecols = ['Milestone', 'ACIO', 'Application', "Start_Date_(Before_CPDs)", "Baseline_Start", "Status_Date"])
date = (data.at[1,'Status_Date']).strftime("%d_%b_%Y")
#remove unnecessary data from the dataframe
rowIndex = []
for index, row in data.iterrows():
	if row['Milestone'] == 'RELEASE' and row['ACIO'][0:1] == 'AD':
		rowIndex.append(index)
	elif row['Milestone'] == 'INITIATIVE' and row['ACIO'][0:1] != 'AD':
		rowIndex.append(index)
	if row['Milestone'] == 'APPLICATION' and row['ACIO'][0:1] != 'AD':
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
		baseline.append((row['ACIO'], row['Application'], days))

for index, row in data.iterrows():
	base = row['Baseline_Start']
	start = row['Start_Date_(Before_CPDs)']
	if not pd.isnull(base) and (base - start).days > 0:
		late.append((row['ACIO'], row['Application'], days))


#convert to dataframes
baseline = pd.DataFrame(sorted(sorted(baseline,key=itemgetter(1)), key=itemgetter(0)), columns = ['ACIO', 'Application', 'Days Past Start Date'])
late = pd.DataFrame(sorted(sorted(late,key=itemgetter(1)), key=itemgetter(0)), columns = ['ACIO', 'Application', 'Days Past Baseline'])

#write to excel
with pd.ExcelWriter('BaselineComparison_'+ date + '.xlsx') as writer:  
	baseline.to_excel(writer, sheet_name = 'No Baseline',index = False)
	late.to_excel(writer, sheet_name = 'Late Start',index = False)

print('Finished')