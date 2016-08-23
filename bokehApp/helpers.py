import pandas as pd

stationMetaData = "bokehApp/data/stationMetadata.csv"


def makeCodesDict():
	"""
	Read stationMetadata.csv file in data directory and return dict of stations in counties
	:rtype: dict of counties keyed by County name and values of Station IDs in that county
	"""
	codesDict = {}
	pdReader = pd.read_csv(stationMetaData)
	pdReader = pdReader[['stid', 'cnty']]
	for index, row in pdReader.iterrows():
		if row['cnty'] in codesDict.keys():
			codesDict[row['cnty']].append(row['stid'])
		else:
			codesDict[row['cnty']] = [row['stid'], ]
	return codesDict


def getStations():
	"""
	Read stationMetadata.csv file in data directory and return dict of stations
	:rtype: dict of stations keyed by station ID and values contain a list of the name of station, county name, latitude and longitude
	"""
	stations = {}
	pdReader = pd.read_csv(stationMetaData)
	pdReader = pdReader[['stid', 'name', 'cnty', 'nlat', 'elon']]
	for index, row in pdReader.iterrows():
		stations[row['stid']] = [row['name'], row['cnty'], row['nlat'], row['elon']]

	return stations
