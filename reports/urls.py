from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Close_The_Box$',Close_The_Box,name="Close_The_Box"),
		url(r'^Invoices$',Invoices,name="Invoices"),
		url(r'^Report_Inventory$',Report_Inventory,name="Report_Inventory"),
		url(r'^Close_The_Box_POS$',Close_The_Box_POS,name="Close_The_Box_POS"),
	]