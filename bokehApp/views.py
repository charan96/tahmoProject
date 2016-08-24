from django.shortcuts import render
from bokeh.models import HoverTool, Label, OpenURL, TapTool
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
import helpers
import pandas as pd


def index(request):
	countyNames, countyCodes, countyX, countyY, codesDict = helpers.countyDataFromBokehSampledata()

	source = ColumnDataSource(data=dict(
		x=countyX,
		y=countyY,
		name=countyNames,
		countyCodes=countyCodes,
	))

	TOOLS = 'pan,tap,reset,box_zoom,hover,save'

	p = figure(title="Oklahoma Counties", tools=TOOLS, plot_width=1000, plot_height=500,
		     x_axis_location=None, y_axis_location=None)
	p.title.text_font_size = '18pt'
	p.title.text_font = 'Bookman'
	p.title.align = 'center'

	p.patches('x', 'y', source=source, fill_color='blue', fill_alpha=0.7, line_color='white',
		    line_width=0.5)
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	# Marking Stations
	# stations = helpers.getStations()
	# for stnID, valList in stations.items():
	# 	p.circle(valList[3], valList[2], size=3, color="yellow")

	hover = p.select_one(HoverTool)
	hover.point_policy = "follow_mouse"
	hover.tooltips = [
		('County', "@name"),
		('Stations', "@countyCodes"),
	]

	url = 'countyMap/@name'
	taptool = p.select(type=TapTool)
	taptool.callback = OpenURL(url=url)

	script, div = components(p)

	return render(request, 'bokehApp/index.html', {"script": script, "div": div})


def countySelect(request, county):
	countyName, countyCodes, countyX, countyY, codesDict = helpers.countyDataFromBokehSampledata(county)

	source = ColumnDataSource(data=dict(
		countyCodes=countyCodes,
	))

	stations = helpers.getStations()

	TOOLS = 'pan,tap,reset,box_zoom,hover,save'

	p = figure(title=countyName, tools=TOOLS, x_axis_location=None, y_axis_location=None)
	p.title.text_font_size = '18pt'
	p.title.text_font = 'Bookman'
	p.title.align = 'center'

	p.patch(countyX, countyY, fill_color='green', fill_alpha=0.7, line_width=0.5)
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	for stnID, valList in stations.items():
		if stnID in countyCodes:
			p.circle(valList[3], valList[2], size=8, color="yellow", source=source)
			p.add_layout(
				Label(x=valList[3], y=valList[2], x_offset=10, y_offset=-5, text=stnID, render_mode='css',
					background_fill_alpha=1.0, border_line_alpha=0, background_fill_color='black',
					text_font='Bookman', text_color="white")
			)

	hover = p.select_one(HoverTool)
	hover.point_policy = "snap_to_data"
	hover.tooltips = [
		('station', '@countyCodes'),
	]

	url = '/station/@countyCodes'
	taptool = p.select(type=TapTool)
	taptool.callback = OpenURL(url=url)

	script, div = components(p)

	return render(request, 'bokehApp/countyMap.html', {"script": script, "div": div, "county": countyName})


def stationPlot(request, station):
	dataMatrix = helpers.getCountyWeatherData(station)


	return render(request, 'bokehApp/stationPlot.html', {})
