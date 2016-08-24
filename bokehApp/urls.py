from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^countyMap/(?P<county>[A-Za-z]+)', views.countySelect, name='countySelect'),
	url(r'^station/(?P<station>[A-Z0-9]+)', views.stationPlot, name='stationPlot'),
]
