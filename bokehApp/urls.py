from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^countyMap/(?P<county>[A-Z][a-z]+)', views.countySelect, name='countySelect'),
]
