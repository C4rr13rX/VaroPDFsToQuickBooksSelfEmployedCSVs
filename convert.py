# Download VARO MONEY transaction history (they will be PDFs) into a folder called Months, or otherwise move them there from their download location
# run this script from its location
# now you have CSV files (they probably call them Excel) to upload to QuickBooks Self Employed in the Cash section of Imports
# if you're monitoring the progress in an open explorer window, once all of the tmp files are gone, it should be done

import csv
import re
import copy
import tabula
import os


months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

for month in months:

	tabula.convert_into("Months/"+month+"2020.pdf", month+"2020.tmp", output_format="csv", pages='all')


for month in months:

	with open(month+"2020.tmp", newline='') as csvfile:
	
		theReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		theReaderList = []
		
		for row in theReader:
			theReaderList.append(row)
			
		counter = 0
		for aRow in theReaderList:
			match = re.search(r'\d+/\d+/\d+?\s',aRow[0])
			if match != None:
				dateMatch = re.search(r'(\d+/\d+/\d+)', aRow[0])
				aRow[0] = dateMatch.group()
				aNewNumber = counter + 1
				theReaderList[aNewNumber][1] = copy.copy(theReaderList[aNewNumber][0])
				theReaderList[aNewNumber][0] = ''
			counter = counter + 1
			
		counter = 0
		for aRow in theReaderList:
			match = re.search(r'(\d+/\d+/\d+)',aRow[0])
			if match != None:
				aRow[1] = copy.copy(theReaderList[counter + 1][1])
				aRow[2] = copy.copy(theReaderList[counter + 1][2])
				theReaderList[counter + 1][0] = ''
				theReaderList[counter + 1][1] = ''
				theReaderList[counter + 1][2] = ''
				theReaderList[counter + 1][3] = ''
			counter = counter + 1
		
		for aRow in theReaderList:
			
			match = re.search(r'(\d+/\d+/\d+)',aRow[0])
			if match == None:
				theReaderList.remove(aRow)
				
		for aRow in theReaderList:
		
			aRow.pop(3)
			if "Ending " in aRow[0]:
				theReaderList.remove(aRow)
				
		with open(month+"2020.csv", 'w') as f:
		
			write = csv.writer(f)
			fields = ['Date','Description','Amount']
			write.writerow(fields)
			write.writerows(theReaderList)
			
for month in months:
	os.remove(month+"2020.tmp")
			
				
		
				
				
				

		