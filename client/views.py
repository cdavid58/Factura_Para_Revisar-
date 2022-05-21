from django.http import HttpResponse
from django.shortcuts import render,redirect
from company.models import Company
from api.translator import Translator
from .models import *
from data.models import Type_Organization,Type_Regime,Municipality,Type_Document_Identification
from api.Create_Client import CreateClient

t = Translator()

def company(request):
	return Company.objects.get(documentIdentification = t.codificar(str((request.session['nit_company']))))


def List_Client(request):
	client = Client.objects.filter(company = company(request))
	_data = [
		{
			'pk':i.pk,
			'document':t.decodificar(str(i.identification_number)),
			'name':t.decodificar(str(i.name)),
			'phone':t.decodificar(str(i.phone)),
			'email':t.decodificar(str(i.email))
		}for i in client
	]
	return render(request,'client/list_client.html',{'c':_data})


def Profile_Client(request,pk):
	client = Client.objects.get(pk = pk)
	data = {
		'pk':client.pk,
		'img':client.img.url,
		'merchant_registration':t.decodificar(str(client.merchant_registration)),
		'name': t.decodificar(str(client.name)),
		'email':t.decodificar(str(client.email)),
		'phone':t.decodificar(str(client.phone)),
		'address':t.decodificar(str(client.address)),
	}
	return render(request,'client/patient-profile.html',{'i':data})

def Add_Client(request):

	global company

	if request.is_ajax():
		data = request.GET
		_client = {
			"identification_number":data['identification_number'] ,
			"dv":data['dv'] ,
			"name":data['name'] ,
			"phone":data['phone'] ,
			"address":data['address'] ,
			"email":data['email'] ,
			"merchant_registration":data['merchant_registration'] ,
			"type_document_identification_id":data['type_document_identification_id'] ,
			"type_organization_id":data['type_organization'] ,
			"type_regime_id":data['type_regime'] ,
			"municipality_id":data['municipality'] ,
			"company":request.session['nit_company']
		}
		c = CreateClient(_client)
		message = c.Create()
		return HttpResponse(message)




	to = Type_Organization.objects.all()
	tr = Type_Regime.objects.all()
	muni = Municipality.objects.all().order_by('name')
	td = Type_Document_Identification.objects.all()
	return render(request,'client/add-patient.html',{'to':to,
		'tr':tr,'muni':muni,'td':td
	})



def Delete_Client(request,pk):
	Client.objects.get(pk = pk).delete()
	return redirect('List_Client')



