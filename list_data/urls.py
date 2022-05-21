from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Electronic_Invoice_List$',Electronic_Invoice_List,name="Electronic_Invoice_List"),
		url(r'^Electronic_Invoice_Docment/(\d+)/$',Electronic_Invoice_Docment,name="Electronic_Invoice_Docment"),
		url(r'^Electronic_Invoice_Docment_POS/(\d+)/$',Electronic_Invoice_Docment_POS,name="Electronic_Invoice_Docment_POS"),
	]