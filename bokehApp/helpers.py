codesCSV = "bokehApp/data/codes.csv"


def makeCodesDict():
	with open(codesCSV, 'r') as infile:
		codesDict = {}
		for line in infile:
			code, countyName = line.rstrip("\n").split(',')
			if countyName in codesDict.keys():
				codesDict[countyName].append(code)
			else:
				codesDict[countyName] = [code, ]
	return codesDict
