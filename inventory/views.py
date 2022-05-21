from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from datetime import date
from api.Create_Inventory import CreateInventory
from empleoyee.models import Empleoyee
from company.models import Company

def c(request):
	return Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))


def Add_Category(request):
	global c
	if request.is_ajax():
		Category(
			name = t.codificar(str(request.GET.get('name')))
		).save()
		return HttpResponse("")

def Add_Inventory(request):
	global c
	category = Category.objects.all()
	
	if request.is_ajax():
		data = request.GET
		print(data)
		_data = {
		    "code":data['code'],
			"name":data['name'],
			"quanty":data['quanty'],
			"price":data['price'],
			"tax":data['tax'],
			"initial_inventory":data['quanty'],
			"subCategories":data['subcategory'],
			"company":request.session['nit_company']
		}
		c_ = CreateInventory(_data)
		message = c_.Create()
		return HttpResponse(message)
	cat = [
		{
			'pk':c.pk,
			'name':t.decodificar(str(c.name))
		}
		for c in category
	]
	return render(request,'inventory/add.html',{'c':cat})

def List_Inventory(request):
	inv = Inventory.objects.filter(company = c(request))
	_data = [
		{
			'pk':i.pk,
			'code': t.decodificar(str(i.code)),
			'description': t.decodificar(str(i.name)),
			'quanty': t.decodificar(str(i.quanty)),
			'tax':t.decodificar(str(i.tax)),
			'price': t.decodificar(str(i.price)),
			

		}
		for i in inv
	]
	return render(request,'inventory/list_inventory.html',{'data':_data})

def Edit_Inventory(request,pk):
	global c
	i = Inventory.objects.get(company = c(request),pk = pk)
	if request.is_ajax():
		data = request.GET
		i.code = t.codificar(str(data['code']))
		i.name = t.codificar(str(data['name']))
		i.price = t.codificar(str(data['price']))
		i.tax = t.codificar(str(data['tax']))
		i.quanty = t.codificar(str(data['quanty']))
		# i.category = Category.objects.get(name = t.codificar(str(data['category'])))
		n = int(t.decodificar(str(i.initial_inventory))) + int(data['quanty'])
		i.initial_inventory = t.codificar(str(n))
		i.save()
		if int(t.decodificar(str(i.quanty))) > 0:
			i.exhausted = False
			i.save()
		Record(
			code = t.codificar(str(data['code'])),
			quanty = t.codificar(str(data['quanty'])),
			price = t.codificar(str(data['price'])),
			tax = t.codificar(str(data['tax'])),
			date = date.today(),
			time = "",
			empleoyee = Empleoyee.objects.get(pk=request.session['empleoyee_pk']),
			company = c(request)
		).save()
		return HttpResponse()
	_data ={
		'pk':i.pk,
		'code': t.decodificar(str(i.code)),
		'description': t.decodificar(str(i.name)),
		'quanty': t.decodificar(str(i.quanty)),
		'tax':t.decodificar(str(i.tax)),
		'price': t.decodificar(str(i.price)),
		# 'category':t.decodificar(str(i.category.name))

	}
	category = Category.objects.all()
	cat = [
		{
			'pk':c.pk,
			'name':t.decodificar(str(c.name))
		}
		for c in category
	]
	print(cat)

	return render(request,'inventory/edit.html',{'i':_data,'c':cat})

def Delete_Inventario(request,pk):
	Inventory.objects.get(pk = pk).delete()
	return redirect("List_Inventory")


def GetSubCategories(request):
	if request.is_ajax():
		import json
		try:
			cate = Category.objects.get(name = t.codificar(str(request.GET.get('pk'))))
			sc = SubCategories.objects.filter(category = cate)
			_data = [
				{
					'pk':i.pk,
					'name':t.decodificar(str(i.name))
				}
				for i in sc
			]
		except Category.DoesNotExist:
			_data = []
		return HttpResponse(json.dumps(_data))
