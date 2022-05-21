from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Wallet_Elec/$',Wallet_Elec,name="Wallet_Elec"),
		url(r'^Report_Wallet_Elec/$',Report_Wallet_Elec,name="Report_Wallet_Elec"),
		url(r'^Electronic_Invoice_Docment_Wallet/(\d+)/$',Electronic_Invoice_Docment_Wallet,name="Electronic_Invoice_Docment_Wallet"),
		url(r'^Wallet_Elec_POS/$',Wallet_Elec_POS,name="Wallet_Elec_POS"),
	]