def calculateUncommon(n):
	arr=["./total-0-0-0.jpg","./total-1-0-1.jpg","./total-1-1-0.jpg","./total-2-0-2.jpg","./total-2-1-1.jpg","./total-2-2-0.jpg","./total-3-0-3.jpg","./total-3-1-2.jpg","./total-3-2-1.jpg","./total-3-3-0.jpg","./total-4-0-4.jpg","./total-4-1-3.jpg","./total-4-2-2.jpg","./total-4-3-1.jpg","./total-4-4-0.jpg","./total-5-0-5.jpg","./total-5-1-4.jpg","./total-5-2-3.jpg","./total-5-3-2.jpg","./total-5-4-1.jpg","./total-5-5-0.jpg","./total-6-0-6.jpg","./total-6-1-5.jpg","./total-6-2-4.jpg","./total-6-3-3.jpg","./total-6-4-2.jpg","./total-6-5-1.jpg","./total-6-6-0.jpg","./total-7-0-7.jpg","./total-7-1-6.jpg","./total-7-2-5.jpg","./total-7-3-4.jpg","./total-7-4-3.jpg","./total-7-5-2.jpg","./total-7-6-1.jpg","./total-7-7-0.jpg","./total-8-0-8.jpg","./total-8-1-7.jpg","./total-8-2-6.jpg","./total-8-3-5.jpg","./total-8-4-4.jpg","./total-8-5-3.jpg","./total-8-6-2.jpg","./total-8-7-1.jpg","./total-8-8-0.jpg","./total-9-0-9.jpg","./total-9-1-8.jpg","./total-9-2-7.jpg","./total-9-3-6.jpg","./total-9-4-5.jpg","./total-9-5-4.jpg","./total-9-6-3.jpg","./total-9-7-2.jpg","./total-9-8-1.jpg","./total-9-9-0.jpg","./total-10-0-10.jpg","./total-10-1-9.jpg","./total-10-2-8.jpg","./total-10-3-7.jpg","./total-10-4-6.jpg","./total-10-5-5.jpg","./total-10-6-4.jpg","./total-10-7-3.jpg","./total-10-8-2.jpg","./total-10-9-1.jpg","./total-10-10-0.jpg","./total-11-0-11.jpg","./total-11-1-10.jpg","./total-11-2-9.jpg","./total-11-3-8.jpg","./total-11-4-7.jpg","./total-11-5-6.jpg","./total-11-6-5.jpg","./total-11-7-4.jpg","./total-11-8-3.jpg","./total-11-9-2.jpg","./total-11-10-1.jpg","./total-11-11-0.jpg","./total-12-0-12.jpg","./total-12-1-11.jpg","./total-12-2-10.jpg","./total-12-3-9.jpg","./total-12-4-8.jpg","./total-12-5-7.jpg","./total-12-6-6.jpg","./total-12-7-5.jpg","./total-12-8-4.jpg","./total-12-9-3.jpg","./total-12-10-2.jpg","./total-12-11-1.jpg","./total-12-12-0.jpg"]
	result = []
	for i in range(len(arr)):
		jpgIndex = arr[i].find(".jpg")
		totalIndex = 8
		a = arr[i][totalIndex:jpgIndex]
		arr2 = a.split("-")
		if arr2[2] == str(n):
			print(a, i)
			result.append(i)
	return result

def calculateCommon(n):
	arr=["./total-0-0-0.jpg","./total-1-0-1.jpg","./total-1-1-0.jpg","./total-2-0-2.jpg","./total-2-1-1.jpg","./total-2-2-0.jpg","./total-3-0-3.jpg","./total-3-1-2.jpg","./total-3-2-1.jpg","./total-3-3-0.jpg","./total-4-0-4.jpg","./total-4-1-3.jpg","./total-4-2-2.jpg","./total-4-3-1.jpg","./total-4-4-0.jpg","./total-5-0-5.jpg","./total-5-1-4.jpg","./total-5-2-3.jpg","./total-5-3-2.jpg","./total-5-4-1.jpg","./total-5-5-0.jpg","./total-6-0-6.jpg","./total-6-1-5.jpg","./total-6-2-4.jpg","./total-6-3-3.jpg","./total-6-4-2.jpg","./total-6-5-1.jpg","./total-6-6-0.jpg","./total-7-0-7.jpg","./total-7-1-6.jpg","./total-7-2-5.jpg","./total-7-3-4.jpg","./total-7-4-3.jpg","./total-7-5-2.jpg","./total-7-6-1.jpg","./total-7-7-0.jpg","./total-8-0-8.jpg","./total-8-1-7.jpg","./total-8-2-6.jpg","./total-8-3-5.jpg","./total-8-4-4.jpg","./total-8-5-3.jpg","./total-8-6-2.jpg","./total-8-7-1.jpg","./total-8-8-0.jpg","./total-9-0-9.jpg","./total-9-1-8.jpg","./total-9-2-7.jpg","./total-9-3-6.jpg","./total-9-4-5.jpg","./total-9-5-4.jpg","./total-9-6-3.jpg","./total-9-7-2.jpg","./total-9-8-1.jpg","./total-9-9-0.jpg","./total-10-0-10.jpg","./total-10-1-9.jpg","./total-10-2-8.jpg","./total-10-3-7.jpg","./total-10-4-6.jpg","./total-10-5-5.jpg","./total-10-6-4.jpg","./total-10-7-3.jpg","./total-10-8-2.jpg","./total-10-9-1.jpg","./total-10-10-0.jpg","./total-11-0-11.jpg","./total-11-1-10.jpg","./total-11-2-9.jpg","./total-11-3-8.jpg","./total-11-4-7.jpg","./total-11-5-6.jpg","./total-11-6-5.jpg","./total-11-7-4.jpg","./total-11-8-3.jpg","./total-11-9-2.jpg","./total-11-10-1.jpg","./total-11-11-0.jpg","./total-12-0-12.jpg","./total-12-1-11.jpg","./total-12-2-10.jpg","./total-12-3-9.jpg","./total-12-4-8.jpg","./total-12-5-7.jpg","./total-12-6-6.jpg","./total-12-7-5.jpg","./total-12-8-4.jpg","./total-12-9-3.jpg","./total-12-10-2.jpg","./total-12-11-1.jpg","./total-12-12-0.jpg"]
	result = []
	for i in range(len(arr)):
		jpgIndex = arr[i].find(".jpg")
		totalIndex = 8
		a = arr[i][totalIndex:jpgIndex]
		arr2 = a.split("-")
		if arr2[1] == str(n):
			print(a, i)
			result.append(i)
	return result

def main():
	run = True
	while(run):
		program = input("1. Common Donation\n2. Uncommon Donation\n 3. Quit\nWhich program? ")
		if program not in ["1", "2", "3"]:
			print("Choose the correct number!\n")
			continue
		if program == "3":
			print("Bye!")
			run = False
		number = input("How many? ")
		if program == "1":
			print(calculateCommon(number))
		elif program == "2":
			print(calculateUncommon(number))


if __name__ == '__main__':
	main()




