from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Update_Payroll_Document/$',Update_Payroll_Document,name="Update_Payroll_Document"),
		url(r'^Send_Payroll/$',Send_Payroll,name="Send_Payroll"),
		url(r'^Recovery_Payroll/$',Recovery_Payroll,name="Recovery_Payroll"),
	]