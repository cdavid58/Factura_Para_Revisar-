from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Empleoyee/$',List_Empleoyee,name="List_Empleoyee"),
		url(r'^Profile_Empleoyee/(\d+)/$',Profile_Empleoyee,name="Profile_Empleoyee"),
		url(r'^Edit_Empleoyee/(\d+)/$',Edit_Empleoyee,name="Edit_Empleoyee"),
		url(r'^Delete_Empleoyee/(\d+)/$',Delete_Empleoyee,name="Delete_Empleoyee"),
		url(r'^Information_Basic/$',Information_Basic,name="Information_Basic"),
		url(r'^Information_Persons/$',Information_Persons,name="Information_Persons"),
		url(r'^Add_Empleoyee/$',Add_Empleoyee,name="Add_Empleoyee"),
	]