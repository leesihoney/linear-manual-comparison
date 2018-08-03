import psycopg2 as pg2
import os
from pathlib import Path

import random
# Establish a connection by specifying the database and user
# This is the psycopg2 analog to
#   %  psql -d postgres -U isdb

con = pg2.connect(database='score', user='isdb')  

con.autocommit = True

# SQL statements are executed via a cursor object
cur = con.cursor()

GENERATION_NUM = 100

def writeFile(pid):
	resultFile = open("%s_linear_manual_comparison.txt" % (pid),"w")
	resultFile.write("%s Score Result \n\n" % (pid))
	matchCount = 0
	tiedCount = 1
	generated_list = []
	while(len(generated_list)<GENERATION_NUM):
		# generating scenarios
		foodType = random.randint(0,1)
		sizeA = random.randint(0,4)
		accessA = random.randint(0,2)
		incomeA = random.randint(0,5)
		povertyA = random.randint(0,6)
		last_donationA = random.randint(1,13)
		total_donationA = random.randint(0,90)
		distanceA = random.randint(0,3)

		sizeB = random.randint(0,4)
		accessB = random.randint(0,2)
		incomeB = random.randint(0,5)
		povertyB = random.randint(0,6)
		last_donationB = random.randint(1,13)
		total_donationB = random.randint(0,90)
		distanceB = random.randint(0,3)

		if last_donationA == 13:
			total_donationA = 0
		elif last_donationB == 12:
			total_donationA = random.randint(1,5)

		if last_donationB == 13:
			total_donationB = 0
		elif last_donationB == 12:
			total_donationB = random.randint(1,5)

		if incomeA == 0:
			povertyA = random.randint(0,4) + 2
		elif incomeA == 1 or incomeA == 2:
			povertyA = random.randint(0,4)
		else:
			povertyA = random.randint(0,2)

		if incomeB == 0:
			povertyB = random.randint(0,4) + 2
		elif incomeB == 1 or incomeB == 2:
			povertyB = random.randint(0,4)
		else:
			povertyB = random.randint(0,2)


		# get linear regression model result
		linear_A = getLinearValue(pid, foodType, sizeA, accessA, incomeA, povertyA, last_donationA, total_donationA, distanceA)
		linear_B = getLinearValue(pid, foodType, sizeB, accessB, incomeB, povertyB, last_donationB, total_donationB, distanceB)
		linearResult = getAlgoChoice(linear_A, linear_B)

		# get manual model result
		manual_A = getManualValue(pid, foodType, sizeA, accessA, incomeA, povertyA, last_donationA, total_donationA, distanceA)
		manual_B = getManualValue(pid, foodType, sizeB, accessB, incomeB, povertyB, last_donationB, total_donationB, distanceB)
		manualResult = getAlgoChoice(manual_A, manual_B)

		if linearResult == None or manualResult == None:
			continue
		
		generated_list.append([foodType, sizeA, accessA, incomeA, povertyA, last_donationA, total_donationA, distanceA, sizeB, accessB, incomeB, povertyB, last_donationB, total_donationB, distanceB])

		resultFile.write("%d.\n" % len(generated_list))
		resultFile.write("Donation Type: %s\n" % (donationString(foodType),))
		resultFile.write("Recipient A\n")
		resultFile.write("Organization Type: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (orgSizeString(sizeA), getSizeLinear(sizeA, pid, foodType), scoreOrgSize(sizeA, foodType, pid)))
		resultFile.write("Food Access: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (foodAccessString(accessA), getAccessLinear(accessA, pid, foodType), scoreFoodAccess(accessA, foodType, pid)))
		resultFile.write("Income Level: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (incomeString(incomeA), getIncomeLinear(incomeA, pid, foodType), scoreIncomeLevel(incomeA, foodType, pid)))
		resultFile.write("Poverty Rate: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (povertyString(povertyA), getPovertyLinear(povertyA, pid, foodType), scorePovertyLevel(povertyA, foodType, pid)))
		if last_donationA == 13:
			resultFile.write("Last Donation Received: Never (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (getLastDonationLinear(last_donationA, pid, foodType), scoreLastDonation(last_donationA, foodType, pid)))
		elif last_donationA == 1:
			resultFile.write("Last Donation Received: 1 week ago (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (getLastDonationLinear(last_donationA, pid, foodType), scoreLastDonation(last_donationA, foodType, pid)))
		else:
			resultFile.write("Last Donation Received: %d weeks ago (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (last_donationA, getLastDonationLinear(last_donationA, pid, foodType), scoreLastDonation(last_donationA, foodType, pid)))	
		commonDonationA, uncommonDonationA = totalDonationInt(total_donationA)
		resultFile.write("Total Donation Received: %d common donation / %d uncommmon donation\n (Linear Regression Model: %f, Manual Scoring Model: %f)" % (commonDonationA, uncommonDonationA, getTotalDonationLinear(total_donationA, pid, foodType), scoreTotalDonation(total_donationA, foodType, pid)))
		resultFile.write("Travel Time: %s minutes\n (Linear Regression Model: %f, Manual Scoring Model: %f)" % (distanceString(distanceA), getDistanceLinear(distanceA, pid, foodType), scoreTravelTime(distanceA, foodType, pid)))

		resultFile.write("\n")

		resultFile.write("Recipient B\n")
		resultFile.write("Organization Type: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (orgSizeString(sizeB), getSizeLinear(sizeB, pid, foodType), scoreOrgSize(sizeB, foodType, pid)))
		resultFile.write("Food Access: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (foodAccessString(accessB), getAccessLinear(accessB, pid, foodType), scoreFoodAccess(accessB, foodType, pid)))
		resultFile.write("Income Level: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (incomeString(incomeB), getIncomeLinear(incomeB, pid, foodType), scoreIncomeLevel(incomeB, foodType, pid)))
		resultFile.write("Poverty Rate: %s (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (povertyString(povertyB), getPovertyLinear(povertyB, pid, foodType), scorePovertyLevel(povertyB, foodType, pid)))
		if last_donationB == 0:
			resultFile.write("Last Donation Received: Never (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (getLastDonationLinear(last_donationB, pid, foodType), scoreLastDonation(last_donationB, foodType, pid)))
		elif last_donationB == 1:
			resultFile.write("Last Donation Received: 1 week ago (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (getLastDonationLinear(last_donationB, pid, foodType), scoreLastDonation(last_donationB, foodType, pid)))
		else:
			resultFile.write("Last Donation Received: %d weeks ago (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (last_donationB, getLastDonationLinear(last_donationB, pid, foodType), scoreLastDonation(last_donationA, foodType, pid)))
		commonDonationB, uncommonDonationB = totalDonationInt(total_donationB)
		resultFile.write("Total Donation Received: %d common donation / %d uncommmon donation (Linear Regression Model: %f, Manual Scoring Model: %f)\n" % (commonDonationB, uncommonDonationB, getTotalDonationLinear(total_donationB, pid, foodType), scoreTotalDonation(total_donationB, foodType, pid)))
		resultFile.write("Travel Time: %s minutes\n (Linear Regression Model: %f, Manual Scoring Model: %f)" % (distanceString(distanceB), getDistanceLinear(distanceB, pid, foodType), scoreTravelTime(distanceB, foodType, pid)))

		resultFile.write("\n")
		resultFile.write("\n")

		# showing result

		resultFile.write("Linear Regression Model: Recipient A(%f) vs Recipient B(%f)\n" % (linear_A, linear_B))
		resultFile.write("Linear Regression Model's Choice: %s\n" % linearResult)

		resultFile.write("\n")

		resultFile.write("Manual Scoring Model: Recipient A(%f) vs Recipient B(%f)\n" % (manual_A, manual_B))
		resultFile.write("Manual Scoring Model's Choice: %s\n" % manualResult)

		resultFile.write("\n")

		resultFile.write("Matched? %s\n" % (linearResult == manualResult))
		resultFile.write("\n")


		# count the # of times when both linear regression model and manual scoring model draw out a same result
		if linearResult == manualResult:
			matchCount+=1

		if linearResult == "Tied" or manualResult == "Tied":
			tiedCount +=1

	resultFile.write("Accuracy: %d/%d\n" % (matchCount, len(generated_list)))
	percentage = (matchCount/len(generated_list))*100
	resultFile.write("Percentage: %0.1f\n" % (percentage,))
	resultFile.write("Tied: %d Scenarios" % (tiedCount,))
	resultFile.close()


def getLinearValue(pid, foodType, size, access, income, poverty, last_donation, total_donation, distance):
	sizeLinear = getSizeLinear(size, pid, foodType)
	accessLinear = getAccessLinear(access, pid, foodType)
	incomeLinear = getIncomeLinear(income, pid, foodType)
	povertyLinear = getPovertyLinear(poverty, pid, foodType)
	lastDonationLinear = getLastDonationLinear(last_donation, pid, foodType)
	totalDonationLinear = getTotalDonationLinear(total_donation, pid, foodType)
	distanceLinear = getDistanceLinear(distance, pid, foodType)

	arr = [sizeLinear, accessLinear, incomeLinear, povertyLinear, lastDonationLinear, totalDonationLinear, distanceLinear]
	if None in arr:
		return None
	return sum(arr)

# linear regression model values
def getSizeLinear(size, pid, foodType):
	beta = getBeta(pid, foodType, "size")
	# encoding size
	if size == 0:
		encoded = 0
	elif size == 1:
		encoded = 0.25
	elif size == 2:
		encoded = 0.5
	elif size == 3:
		encoded = 0.75
	else:
		encoded = 1 
	return beta * encoded

def getAccessLinear(access, pid, foodType):
	beta = getBeta(pid, foodType, "access")
	# encoding access
	if access == 0:
		encoded = 0
	elif access == 1:
		encoded = 0.5
	else:
		encoded = 1
	return beta * encoded

def getIncomeLinear(income, pid, foodType):
	beta = getBeta(pid, foodType, "income")
	# encoding income
	if income == 0:
		encoded = 1 / 5.0
	elif income == 1:
		encoded = 2 / 5.0
	elif income == 2:
		encoded = 3 / 5.0
	elif income == 3:
		encoded = 4 / 5.0
	else: 
		encoded = 1
	return beta * encoded

def getPovertyLinear(poverty, pid, foodType):
	beta = getBeta(pid, foodType, "poverty")
	# encoding poverty
	if poverty == 0:
		encoded = 0
	elif poverty == 1: 
		encoded = 1/6.0
	elif poverty == 2:
		encoded = 2/6.0
	elif poverty == 3:
		encoded = 3/6.0
	elif poverty == 4:
		encoded = 4/6.0
	elif poverty == 5:
		encoded = 5/6.0
	else:
		encoded = 1
	return beta * encoded

def getDistanceLinear(distance, pid, foodType):
	beta = getBeta(pid, foodType, "distance")
	# encoding distance
	if distance == 0:
		encoded = 0
	elif distance == 1:
		encoded = 1/3.0
	elif distance == 2:
		encoded = 2/3.0
	else:
		encoded = 1
	return beta * encoded

def getLastDonationLinear(lastD, pid, foodType):
	beta = getBeta(pid, foodType, "last_donation")
	# encoding last donaton 
	if lastD == 13:
		encoded = 1
	else: 
		encoded = (lastD-1)/12
	return beta * encoded

def getTotalDonationLinear(totalD, pid, foodType):
	betaSame = getBeta(pid, foodType, "same_donation")
	betaDiff = getBeta(pid, foodType, "different_donation")
	# divide common donation and linear donation

	# common donation part
	if totalD in [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]: # when common donation = 0
		commonDonation = 0
	elif totalD in [2, 4, 7, 11, 16, 22, 29, 37, 46, 56, 67, 79]: # when common donation = 1
		commonDonation = 1
	elif totalD in [5, 8, 12, 17, 23, 30, 38, 47, 57, 68, 80]:
		commonDonation = 2
	elif totalD in [9, 13, 18, 24, 31, 39, 48, 58, 69, 81]:
		commonDonation = 3
	elif totalD in [14, 19, 25, 32, 40, 49, 59, 70, 82]:
		commonDonation = 4
	elif totalD in [20, 26, 33, 41, 50, 60, 71, 83]:
		commonDonation = 5
	elif totalD in [27, 34, 42, 51, 61, 72, 84]:
		commonDonation = 6
	elif totalD in [35, 43, 52, 62, 73, 85]:
		commonDonation = 7
	elif totalD in [44, 53, 63, 74, 86]:
		commonDonation = 8
	elif totalD in [54, 64, 75, 87]:
		commonDonation = 9
	elif totalD in [65, 76, 88]:
		commonDonation = 10
	elif totalD in [77, 89]:
		commonDonation = 11
	else:
		commonDonation = 12

	# uncommmon donation
	if totalD in [0, 2, 5, 9, 14, 20, 27, 35, 44, 54, 65, 77, 90]: # when common donation = 0
		uncommonDonation = 0
	elif totalD in [1, 4, 8, 13, 19, 26, 34, 43, 53, 64, 76, 89]: # when common donation = 1
		uncommonDonation = 1
	elif totalD in [3, 7, 12, 18, 25, 33, 42, 52, 63, 75, 88]:
		uncommonDonation = 2
	elif totalD in [6, 11, 17, 24, 32, 41, 51, 62, 74, 87]:
		uncommonDonation = 3
	elif totalD in [10, 16, 23, 31, 40, 50, 61, 73, 86]:
		uncommonDonation = 4
	elif totalD in [15, 22, 30, 39, 49, 60, 72, 85]:
		uncommonDonation = 5
	elif totalD in [21, 29, 38, 48, 59, 71, 84]:
		uncommonDonation = 6
	elif totalD in [28, 37, 47, 58, 70, 83]:
		uncommonDonation = 7
	elif totalD in [36, 46, 57, 69, 82]:
		uncommonDonation = 8
	elif totalD in [45, 56, 68, 81]:
		uncommonDonation = 9
	elif totalD in [55, 67, 80]:
		uncommonDonation = 10
	elif totalD in [66, 79]:
		uncommonDonation = 11
	else:
		uncommonDonation = 12

	# encode common and uncommon donation values
	if commonDonation >= 12:
		commonEncoded = 1
	else:
		commonEncoded = commonDonation/12.0

	if uncommonDonation >= 12:
		uncommonEncoded = 1
	else:
		uncommonEncoded = uncommonDonation/12.0

	# get linear regression data

	if foodType == 0: # when common donation
		return betaSame * commonEncoded + betaDiff * uncommonEncoded
	else:
		return betaSame * uncommonEncoded + betaDiff * commonEncoded

def getBeta(pid, foodType, column):
	selectQuery = '''SELECT %s''' % (column,)
	fromQuery = ''' FROM beta_values'''
	whereQuery = ''' WHERE donation_type = (%s) and pid = (%s)'''

	query = selectQuery + fromQuery + whereQuery

	return executeQuery(query, (foodType, pid))

def getManualValue(pid, foodType, size, access, income, poverty, last_donation, total_donation, distance):
	sizeManual = scoreOrgSize(size, foodType, pid)
	accessManual = scoreFoodAccess(access, foodType, pid)
	incomeManual = scoreIncomeLevel(income, foodType, pid)
	povertyManual = scorePovertyLevel(poverty, foodType, pid)
	lastDonationManual = scoreLastDonation(last_donation, foodType, pid)
	totalDonationManual = scoreTotalDonation(total_donation, foodType, pid)
	distanceManual = scoreTravelTime(distance, foodType, pid)

	arr = [sizeManual, accessManual, povertyManual, lastDonationManual, totalDonationManual, distanceManual]

	if None in arr:
		return None
	return sum(arr)

def donationString(foodType):
	if foodType == 0:
		return "Common Donation"
	elif foodType == 1:
		return "Uncommon Donation"

def orgSizeString(size):
	if size == 0:
		return "Less Than 50 Clients"
	if size == 1:
		return "50 - 100 Clients"
	if size == 2:
		return "100 - 500 Clients"
	if size == 3:
		return "500 - 1000 Clients"
	else:
		return "More Than 1000 Clients"

def foodAccessString(access):
	if access == 0:
		return "Normal"
	if access == 1:
		return "Low"
	if access == 2:
		return "Extremely Low"

def incomeString(income):
	if income == 0:
		return "0 - 20k"
	if income == 1:
		return "20 - 40k"
	if income == 2:
		return "40 - 60k"
	if income == 3:
		return "60 - 80k"
	if income == 4:
		return "80 - 100k"
	return "100k+"

def povertyString(poverty):
	if poverty == 0:
		return "0 - 10%"
	if poverty == 1:
		return "10 - 20%"
	if poverty == 2:
		return "20 - 30%"
	if poverty == 3:
		return "30 - 40%"
	if poverty == 4:
		return "40 - 50%"
	if poverty == 5:
		return "50 - 60%"
	return "60+%"

def totalDonationInt(totalD):
	if totalD in [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]: # when common donation = 0
		commonDonation = 0
	elif totalD in [2, 4, 7, 11, 16, 22, 29, 37, 46, 56, 67, 79]: # when common donation = 1
		commonDonation = 1
	elif totalD in [5, 8, 12, 17, 23, 30, 38, 47, 57, 68, 80]:
		commonDonation = 2
	elif totalD in [9, 13, 18, 24, 31, 39, 48, 58, 69, 81]:
		commonDonation = 3
	elif totalD in [14, 19, 25, 32, 40, 49, 59, 70, 82]:
		commonDonation = 4
	elif totalD in [20, 26, 33, 41, 50, 60, 71, 83]:
		commonDonation = 5
	elif totalD in [27, 34, 42, 51, 61, 72, 84]:
		commonDonation = 6
	elif totalD in [35, 43, 52, 62, 73, 85]:
		commonDonation = 7
	elif totalD in [44, 53, 63, 74, 86]:
		commonDonation = 8
	elif totalD in [54, 64, 75, 87]:
		commonDonation = 9
	elif totalD in [65, 76, 88]:
		commonDonation = 10
	elif totalD in [77, 89]:
		commonDonation = 11
	else:
		commonDonation = 12

	# uncommmon donation
	if totalD in [0, 2, 5, 9, 14, 20, 27, 35, 44, 54, 65, 77, 90]: # when common donation = 0
		uncommonDonation = 0
	elif totalD in [1, 4, 8, 13, 19, 26, 34, 43, 53, 64, 76, 89]: # when common donation = 1
		uncommonDonation = 1
	elif totalD in [3, 7, 12, 18, 25, 33, 42, 52, 63, 75, 88]:
		uncommonDonation = 2
	elif totalD in [6, 11, 17, 24, 32, 41, 51, 62, 74, 87]:
		uncommonDonation = 3
	elif totalD in [10, 16, 23, 31, 40, 50, 61, 73, 86]:
		uncommonDonation = 4
	elif totalD in [15, 22, 30, 39, 49, 60, 72, 85]:
		uncommonDonation = 5
	elif totalD in [21, 29, 38, 48, 59, 71, 84]:
		uncommonDonation = 6
	elif totalD in [28, 37, 47, 58, 70, 83]:
		uncommonDonation = 7
	elif totalD in [36, 46, 57, 69, 82]:
		uncommonDonation = 8
	elif totalD in [45, 56, 68, 81]:
		uncommonDonation = 9
	elif totalD in [55, 67, 80]:
		uncommonDonation = 10
	elif totalD in [66, 79]:
		uncommonDonation = 11
	else:
		uncommonDonation = 12	
	return commonDonation, uncommonDonation

def distanceString(distance):
	if distance == 0:
		return "15"
	if distance == 1:
		return "30"
	if distance == 2:
		return "45"
	return "60+"

def executeQuery(query, columnTuple):
	cur.execute(query, columnTuple)
	ans = cur.fetchall()
	if len(ans) == 1:
		return ans[0][0]
	else:
		return None

def scoreOrgSize(org, donation, person):
	if org == 0:
		query = '''SELECT fifty 
				 	 FROM organization_size
					WHERE person = (%s) and food_type = (%s)'''

	elif org == 1:
		query = '''SELECT hundred
				 	 FROM organization_size
					WHERE person = (%s) and food_type = (%s)'''

	elif org == 2:
		query = '''SELECT fiveHundred 
					 FROM organization_size
					WHERE person = (%s) and food_type = (%s)'''

	elif org == 3:
		query = '''SELECT thousand 
					 FROM organization_size
					WHERE person = (%s) and food_type = (%s)'''

	elif org == 4:
		query = '''SELECT larger
					 FROM organization_size
					WHERE person = (%s) and food_type = (%s)'''

	return executeQuery(query, (person, donation))

def scoreFoodAccess(foodAccess, donation, person):
	if foodAccess == 0:
		query = '''SELECT normal
					 FROM food_access
					WHERE person = (%s) and food_type = (%s)'''

	elif foodAccess == 1:
		query = '''SELECT low
					 FROM food_access
					WHERE person = (%s) and food_type = (%s)'''

	elif foodAccess == 2:
		query = '''SELECT extremely_low
					 FROM food_access
					WHERE person = (%s) and food_type = (%s)'''
	return executeQuery(query, (person, donation))


def scoreIncomeLevel(incomeLevel, donation, person):
	if incomeLevel == 0:
		query = '''SELECT zeroK
					 FROM income
					WHERE person = (%s) and food_type = (%s)'''

	elif incomeLevel == 1:
		query = '''SELECT twentyK
					 FROM income
					WHERE person = (%s) and food_type = (%s)'''	

	elif incomeLevel == 2:
		query = '''SELECT fourtyK
					 FROM income
					WHERE person = (%s) and food_type = (%s)'''

	elif incomeLevel == 3:
		query = '''SELECT sixtyK 
					 FROM income
					WHERE person = (%s) and food_type = (%s)'''

	elif incomeLevel == 4:
		query = '''SELECT eightyK
				 	FROM income
					WHERE person = (%s) and food_type = (%s)'''

	elif incomeLevel == 5:
		query = '''SELECT hundredK
					 FROM income
					WHERE person = (%s) and food_type = (%s)'''

	return executeQuery(query, (person, donation))


def scorePovertyLevel(poverty, donation, person):
	if poverty == 0:
		query = '''SELECT zero
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''

	elif poverty == 1:
		query = '''SELECT ten 
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''
	elif poverty == 2:
		query = '''SELECT twenty
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''

	elif poverty == 3:
		query = '''SELECT thirty
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''

	elif poverty == 4:
		query = '''SELECT forty
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''

	elif poverty == 5:
		query = '''SELECT fifty
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''
	elif poverty == 6:
		query = '''SELECT sixty
					 FROM poverty
					WHERE person = (%s) and food_type = (%s)'''

	return executeQuery(query, (person, donation))


def scoreLastDonation(lastD, donation, person):
	if lastD == 0:
		return None
	if lastD == 1:
		query = '''SELECT one
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 2:
		query = '''SELECT two 
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 3:
		query = '''SELECT three
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 4:
		query = '''SELECT four
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 5:
		query = '''SELECT five
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 6:
		query = '''SELECT six 
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 7:
		query = '''SELECT seven
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 8:
		query = '''SELECT eight
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 9:
		query = '''SELECT nine
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 10:
		query = '''SELECT ten 
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 11:
		query = '''SELECT eleven 
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 12:
		query = '''SELECT twelve
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	elif lastD == 13:
		query = '''SELECT never
					 FROM lastDonation
					WHERE person = (%s) and food_type = (%s)'''

	return executeQuery(query, (person, donation))



def scoreTotalDonation(totalD, donation, person):
	if totalD == 0:
		query = '''SELECT zero
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [1,2]:
		query = '''SELECT one 
					 FROM totalDonation
					WHERE person = (%s)'''	

	elif totalD in [3,4,5]:
		query = '''SELECT two
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [6,7,8,9]:
		query = '''SELECT three
					 FROM totalDonation
					WHERE person = (%s)'''
	elif totalD in [10,11,12,13,14]:
		query = '''SELECT four 
					 FROM totalDonation
					WHERE person = (%s)'''


	elif totalD in [15,16,17,18,19,20]:
		query = '''SELECT five
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [21,22,23,24,25,26,27]:
		query = '''SELECT six
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [28,29,30,31,32,33,34,35]:
		query = '''SELECT seven
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [36,37,38,39,40,41,42,43,44]:
		query = '''SELECT eight
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [45,46,47,48,49,50,51,52,53,54]:
		query = '''SELECT nine
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [55,56,57,58,59,60,61,62,63,64,65]:
		column = "ten"
		query = '''SELECT ten 
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [66,67,68,69,70,71,72,73,74,75,76,77]:
		column = "eleven"
		query = '''SELECT eleven 
					 FROM totalDonation
					WHERE person = (%s)'''

	elif totalD in [78,79,80,81,82,83,84,85,86,87,88,89,90]:
		query = '''SELECT twelve
					 FROM totalDonation
					WHERE person = (%s)'''

	return executeQuery(query, (person,))


def scoreTravelTime(travel, donation, person):
	if travel == 0:
		query = '''SELECT fifteen
					 FROM distance
					WHERE person = (%s) and food_type = (%s)'''

	elif travel == 1:
		query = '''SELECT thirty
					 FROM distance
					WHERE person = (%s) and food_type = (%s)'''

	elif travel == 2:
		query = '''SELECT fourtyFive
					 FROM distance
					WHERE person = (%s) and food_type = (%s)'''

	elif travel == 3:
		query = '''SELECT sixty
					 FROM distance
					WHERE person = (%s) and food_type = (%s)'''

	return executeQuery(query, (person, donation))


def getAlgoChoice(sumA, sumB):
	if sumA == None or sumB == None:
		return None
	if sumA > sumB:
		return 'A'
	elif sumB > sumA:
		return 'B'
	else:
		return 'Tied'

def main():
	run = True
	while(run):
		pid = input("Enter The PID (Press '#' if you wish to Quit): ")
		# quitting scenario
		if pid == '#':
			print('Exiting...')
			run = False
			break

		# checking beta values of pid
		betaSql = '''SELECT *
			 		   FROM beta_values
					  WHERE pid = (%s)'''
		cur.execute(betaSql, (pid,))
		betaExecute = cur.fetchall()
		if len(betaExecute) == 0: 
			print("There is no corresponding PID called %s in beta_values table\n" % (pid,))
			continue

		# checking scores of pid for each factor
		failedArray = []
		sqlArray = ['distance', 'food_access', 'income', 'lastDonation', 'organization_size', 'poverty', 'totalDonation', 'totalDonationCommon', 'totalDonationUncommon']
		for table in sqlArray:
			scoreSql = '''SELECT *
						    FROM %s''' % (table, )
						   
			cur.execute(''+ scoreSql + ' WHERE person = (%s)' , (pid, ))
			scoreExecute = cur.fetchall()
			if len(scoreExecute) == 0:
				print("There is no corresponding PID called %s in %s table\n" % (pid, table))
				failedArray.append(table)
				continue

		if len(failedArray) != 0:
			continue

		# run the program
		print("Writing %s Linear Regression Model & Manual Scoring Model Results..." % (pid,))
		writeFile(pid)
		print("Done!!!")

if __name__ == '__main__':
	main()


