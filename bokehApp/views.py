from django.shortcuts import render
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.sampledata.us_counties import data as counties
from bokeh.embed import components
import helpers


# Create your views here.
def index(request):
	oklahomaCounties = {code: county for code, county in counties.items() if county['state'] == 'ok'}

	codesDict = helpers.makeCodesDict()
	stations = helpers.getStations()

	countyNames = [county['name'] for county in oklahomaCounties.values()]
	countyX = [county['lons'] for county in oklahomaCounties.values()]
	countyY = [county['lats'] for county in oklahomaCounties.values()]
	countyCodes = [codesDict[county] for county in countyNames]

	source = ColumnDataSource(data=dict(
		x=countyX,
		y=countyY,
		name=countyNames,
		stns=stations.keys(),
		cty=[ct[1] for ct in stations.values()],
		countyCodes=countyCodes,
	))

	TOOLS = 'pan,reset,box_zoom,hover,save'

	p = figure(title="Oklahoma Counties", tools=TOOLS, plot_width=1000, plot_height=500, x_axis_location=None,
		     y_axis_location=None)
	p.patches('x', 'y', source=source, fill_color='blue', fill_alpha=0.7, line_color='white', line_width=0.5)
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	# Marking Stations
	# for stnID, valList in stations.items():
	# 	p.circle(valList[3], valList[2], size=3, color="yellow")
	# p.circle(-97.5085, 35.4819, size=3, color="yellow")

	hover = p.select_one(HoverTool)
	hover.point_policy = "follow_mouse"
	hover.tooltips = [
		('County', "@name"),
		('Stations', "@countyCodes"),
	]

	script, div = components(p)

	return render(request, 'bokehApp/index.html', {"script": script, "div": div})
