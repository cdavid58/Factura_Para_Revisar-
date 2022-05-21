from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Invoice_POS/$',List_Invoice_POS,name="List_Invoice_POS"),
		url(r'^Create_POS/$',Create_POS,name="Create_POS"),
		url(r'^Payment_Forms_POS/$',Payment_Forms_POS,name="Payment_Forms_POS"),
		url(r'^Save_Invoice_Pos/$',Save_Invoice_Pos,name="Save_Invoice_Pos"),
		url(r'^Vence_Pos/$',Vence_Pos,name="Vence_Pos"),
		url(r'^GetProducts_POS/$',GetProducts_POS,name="GetProducts_POS"),
		url(r'^Print_Invoice/$',Print_Invoice,name="Print_Invoice"),
		url(r'^Credit_Notes/$',Credit_Notes,name="Credit_Notes"),
		url(r'^List_Credit_Note_POS/$',List_Credit_Note_POS,name="List_Credit_Note_POS"),
		url(r'^GetPDF_POS/(\d)+/$',GetPDF_POS,name="GetPDF_POS"),
	]