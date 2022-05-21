from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Invoice/$',List_Invoice,name="List_Invoice"),
		url(r'^Create_Invoice/$',Create_Invoice,name="Create_Invoice"),
		url(r'^GetProducts/$',GetProducts,name="GetProducts"),
		url(r'^Save_Invoice_FE/$',Save_Invoice_FE,name="Save_Invoice_FE"),
		url(r'^Payment_Forms/$',Payment_Forms,name="Payment_Forms"),
		url(r'^Vence/$',Vence,name="Vence"),
		url(r'^Print_Invoice/$',Print_Invoice,name="Print_Invoice"),
		url(r'^Send_Dian/(\d+)/$',Send_Dian,name="Send_Dian"),
		url(r'^Credit_Notes/(\d+)/$',Credit_Notes,name="Credit_Notes"),
		url(r'^NoteCreditProduct/$',NoteCreditProduct,name="NoteCreditProduct"),
		url(r'^List_Credit_Note/$',List_Credit_Note,name="List_Credit_Note"),
	]