from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Add_Inventory/$',Add_Inventory,name="Add_Inventory"),
		url(r'^List_Inventory/$',List_Inventory,name="List_Inventory"),
		url(r'^Add_Category/$',Add_Category,name="Add_Category"),
		url(r'^Edit_Inventory/(\d+)/$',Edit_Inventory,name="Edit_Inventory"),
		url(r'^Delete_Inventario/(\d+)/$',Delete_Inventario,name="Delete_Inventario"),
		url(r'^GetSubCategories/$',GetSubCategories,name="GetSubCategories"),
	]