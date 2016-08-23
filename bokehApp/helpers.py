import pandas as pd
from bokeh.sampledata.us_counties import data as counties

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


def countyDataFromBokehSampledata(*args):
	codesDict = makeCodesDict()
	oklahomaCounties = {code: county for code, county in counties.items() if county['state'] == 'ok'}

	countyNames = [county['name'] for county in oklahomaCounties.values()]
	# Replacing Le Flore with LeFlore to account for the difference in spelling the bokeh sample data and the metadata
	idx = countyNames.index("Le Flore")
	countyNames.remove("Le Flore")
	countyNames.insert(idx, "LeFlore")

	countyX = [county['lons'] for county in oklahomaCounties.values()]
	countyY = [county['lats'] for county in oklahomaCounties.values()]
	listOfStnsInEachCounty = [codesDict[county] for county in countyNames]

	if len(args) == 0:
		return countyNames, listOfStnsInEachCounty, countyX, countyY, codesDict
	elif len(args) == 1:
		county = args[0]
		idx = countyNames.index(county)

		return countyNames[idx], listOfStnsInEachCounty[idx], countyX[idx], countyY[idx], codesDict
	else:
		return None, None, None, None, None

	# return countyNames, listOfStnsInEachCounty, countyX, countyY, codesDict
