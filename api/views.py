from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
# from .serializer import *
import base64
from .Create_Company import CreateCompany
from .Create_Client import CreateClient
from .Create_Category import Create_Category_
from .Create_Inventory import CreateInventory
from .Create_POS import CreateInvoicePos
from .Create_Empleoyee_ import CreateEmpleoyee
from .Create_Seller import CreateSeller
from .Create_Invoice import *
from .Create_POS import *
from .SendInvoiceDian import send_invoice_dian
from invoice.models import Invoice
from seller.models import Seller
from django.utils.crypto import get_random_string

@api_view(['POST'])
def Create_Company(request):
	data = request.data
	token = get_random_string(length=96)
	passwd = get_random_string(length=96)
	c = CreateCompany(data,token,passwd)
	message = c.Create()
	_message = {'Message':message}
	if message == "Successfully registered company":
		_message = {'Message':message,'Token':token,'Passwd':passwd}
	return Response(_message)

@api_view(['POST'])
def Create_Client(request):
	data = request.data
	c = CreateClient(data)
	message = c.Create()
	return Response({'Message':message})

@api_view(['POST'])
def Create_Invoice_(request):
	data = request.data
	c = CreateInvoice(data)
	c.Create_Invoice_Lines()
	message = c.Create_Payment_Form()
	return Response({'Message':message})


@api_view(['POST'])
def Create_Payroll(request):
	data = request.data
	return Response({'Message':data})

@api_view(['POST'])
def Create_Category(request):
	data = request.data
	c = Create_Category_(data)
	message = c.Create()
	return Response({'Message':message})

@api_view(['POST'])
def CreateSubCategories(request):
	data = request.data
	from inventory.models import SubCategories,Category
	SubCategories(
		name = t.codificar(str(data['name'])),
		category = Category.objects.get(pk = data["id_category"])
	).save()
	return Response({'Message':data})


@api_view(['POST'])
def Create_Inventory(request):
	data = request.data
	c = CreateInventory(data)
	message = c.Create()
	return Response({'Message':message})

@api_view(['POST'])
def Create_Empleoyee(request):
	data = request.data
	message = ""
	c = CreateEmpleoyee(data)
	passwd = get_random_string(length=96)
	message = c.Create(passwd)
	if message == "The company is not registered":
		return Response({'Message':message})
	return Response({'Message':message,'Passwd':passwd})


@api_view(['POST'])
def Create_POS_Invoice(request):
	data = request.data
	c = CreateInvoicePos(data)
	c.Create_Invoice_Lines()
	message = c.Create_Payment_Form()
	return Response({'Message':message})


###########################################################################+

@api_view(['POST'])
def Send_Invoice_DIAN(request):
	data = request.data
	c = send_invoice_dian(data['number'],12345678990)
	message = c.Send_Electronic_Invoice()
	return Response({'Message':message})


@api_view(['POST'])
def Delete_Company(request):
	company = Company.objects.all()
	for i in company:
		i.delete()
	message = "successful deletion"
	return Response({'Message':message})

@api_view(['POST'])
def Create_Sellers(request):
	data = request.data 
	c = CreateSeller(data)
	message = c.Register()
	return Response({'Message':message})



@api_view(['POST'])
def Delete_Seller(request):
	seller = Seller.objects.all()
	for i in seller:
		i.delete()
	message = "successful deletion"
	return Response({'Message':message})



###############################################################

@api_view(['GET'])
def GetAllCompanies(request):
	data = request.data
	list_companies = []
	companies = Company.objects.all()
	for i in companies:
		list_companies.append({
			'documentIdentification':t.decodificar(str(i.documentIdentification)),
			'type_documentI':i.type_documentI.name,
			'type_organization':i.type_organization.name,
			'type_regime':i.type_regime.name,
			'business_name':t.decodificar(str(i.business_name)),
			'municipality':i.municipality.name,			
			'address':t.decodificar(str(i.address)),
			'phone':t.decodificar(str(i.phone)),
			'email':t.decodificar(str(i.email)),
			'certificate_generation_date':i.certificate_generation_date,
			'certificate_expiration_date':i.certificate_expiration_date,
			'resolution_generation_date':i.resolution_generation_date,
			'resolution_expiration_date':i.resolution_expiration_date,
			'block':i.block,
			'token':t.decodificar(str(i.token)),
			'user':t.decodificar(str(i.user)),
			'password':t.decodificar(str(i.password)),
			'cod_bars':i.cod_bars,
			'resolution_number':i.resolution_number,
			'prefix':i.prefix,
			'license':i.license,
			'date_register':i.date_register,
			'payment_date':i.payment_date
			})
	return Response({'All Companies':list_companies})



@api_view(['POST'])
def Delete_Client(request):
	from client.models import Client
	Client.objects.get(identification_number = t.codificar(request.data['identification_number'])).delete()
	return Response({'Message':'The client was successfully removed'})

@api_view(['POST'])
def Delete_All_Invoices_POS(request):
	from pos.models import POS
	pos = POS.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.data['company']))))
	for i in pos:
		i.delete()
	return Response({'Message':'Invoice Delete'})






