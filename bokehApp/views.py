from django.shortcuts import render
from bokeh.models import HoverTool, Range1d
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.sampledata.us_counties import data as counties
from bokeh.embed import components
import helpers, random


def index(request):
	countyNames, countyCodes, countyX, countyY, codesDict = helpers.countyDataFromBokehSampledata()

	# stations = helpers.getStations()

	source = ColumnDataSource(data=dict(
		x=countyX,
		y=countyY,
		name=countyNames,
		countyCodes=countyCodes,
	))

	TOOLS = 'pan,reset,box_zoom,hover,save'

	p = figure(title="Oklahoma Counties", tools=TOOLS, plot_width=1000, plot_height=500,
		     x_axis_location=None, y_axis_location=None)
	p.title.text_font_size = '12pt'

	p.patches('x', 'y', source=source, fill_color='blue', fill_alpha=0.7, line_color='white', line_width=0.5)
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	# Marking Stations
	# for stnID, valList in stations.items():
	# 	p.circle(valList[3], valList[2], size=3, color="yellow")

	hover = p.select_one(HoverTool)
	hover.point_policy = "follow_mouse"
	hover.tooltips = [
		('County', "@name"),
		('Stations', "@countyCodes"),
	]

	script, div = components(p)

	return render(request, 'bokehApp/index.html', {"script": script, "div": div})


def countySelect(request, county):
	countyName, countyCodes, countyX, countyY, codesDict = helpers.countyDataFromBokehSampledata(county)

	stations = helpers.getStations()

	source = ColumnDataSource(data=dict(
		x=countyX,
		y=countyY,
		name=countyName,
		countyCodes=countyCodes,
	))

	TOOLS = 'pan,reset,box_zoom,hover,save'

	p = figure(title=countyName, tools=TOOLS, plot_width=1000, plot_height=500)
	p.title.text_font_size = '12pt'

	p.patch(countyX, countyY, fill_color='blue', fill_alpha=0.7, line_width=0.5)
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	for stnID, valList in stations.items():
		if stnID in countyCodes:
			p.circle(valList[3], valList[2], size=5, color="yellow")

	hover = p.select_one(HoverTool)
	hover.point_policy = "follow_mouse"
	hover.tooltips = [
		('Stations', "@countyCodes"),
	]

	script, div = components(p)

	return render(request, 'bokehApp/countyMap.html', {"script": script, "div": div})
