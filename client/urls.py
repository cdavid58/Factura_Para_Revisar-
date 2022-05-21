from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Client$',List_Client,name="List_Client"),
		url(r'^Profile_Client/(\d+)/$',Profile_Client,name="Profile_Client"),
		url(r'^Delete_Client/(\d+)/$',Delete_Client,name="Delete_Client"),
		url(r'^Add_Client/$',Add_Client,name="Add_Client"),
	]