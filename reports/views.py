from django.shortcuts import render
from invoice.models import *
from datetime import date
from api.translator import Translator
from inventory.models import Inventory
from pos.models import *

t = Translator()


def Close_The_Box(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())))
	number_invoice = []
	for i in invoice:
		if int(t.decodificar(str(i.number))) not in number_invoice:
			number_invoice.append(int(t.decodificar(str(i.number))))
	_data = []
	for j in number_invoice:
		_i = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())), number = t.codificar(str(j)))
		subtotal = 0
		tax = 0
		discount = 0
		cost = 0
		total = 0
		for i_ in _i:
			cost += i_.Base_Product_WithOut_Discount()
			subtotal += i_.Base_Product_WithOut_Discount() * float(t.decodificar(str(i_.quanty)))
			tax += i_.Tax_Value()
			total += i_.Totals()
		_data.append({
			'number':j,
			'cost': cost,
			'subtotal':subtotal,
			'discount':discount,
			'tax':tax,
			'totals':total,
			'date':str(date.today())
			})
	return render(request,'reports/close_the_box.html',{'data':_data})

def Invoices(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())))
	number_invoice = []
	subtotal = 0
	tax = 0
	discount = 0
	cost = 0
	total = 0
	_data = []
	for i_ in invoice:
		cost += i_.Base_Product_WithOut_Discount()
		subtotal += i_.Base_Product_WithOut_Discount() * float(t.decodificar(str(i_.quanty)))
		tax += i_.Tax_Value()
		total += i_.Totals()
		_data.append({
			'number':'N-'+str(t.decodificar(str(i_.number))),
			'cost': cost,
			'subtotal':subtotal,
			'discount':discount,
			'tax':tax,
			'totals':total,
			'date':str(date.today())
			})
	return render(request,'reports/invoice.html',{'data':_data})


def Close_The_Box_POS(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())))
	number_invoice = []
	for i in invoice:
		if int(t.decodificar(str(i.number))) not in number_invoice:
			number_invoice.append(int(t.decodificar(str(i.number))))
	_data = []
	for j in number_invoice:
		_i = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())), number = t.codificar(str(j)))
		subtotal = 0
		tax = 0
		discount = 0
		cost = 0
		total = 0
		for i_ in _i:
			cost += i_.Base_Product_WithOut_Discount()
			subtotal += i_.Base_Product_WithOut_Discount() * float(t.decodificar(str(i_.quanty)))
			tax += i_.Tax_Value()
			total += i_.Totals()
		_data.append({
			'number':j,
			'cost': cost,
			'subtotal':subtotal,
			'discount':discount,
			'tax':tax,
			'totals':total,
			'date':str(date.today())
			})
	return render(request,'reports/close_the_box.html',{'data':_data})

def Invoices_pos(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())))
	number_invoice = []
	subtotal = 0
	tax = 0
	discount = 0
	cost = 0
	total = 0
	_data = []
	for i_ in invoice:
		cost += i_.Base_Product_WithOut_Discount()
		subtotal += i_.Base_Product_WithOut_Discount() * float(t.decodificar(str(i_.quanty)))
		tax += i_.Tax_Value()
		total += i_.Totals()
		_data.append({
			'number':'N-'+str(t.decodificar(str(i_.number))),
			'cost': cost,
			'subtotal':subtotal,
			'discount':discount,
			'tax':tax,
			'totals':total,
			'date':str(date.today())
			})
	return render(request,'reports/invoice.html',{'data':_data})


def Report_Inventory(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	inventory = Inventory.objects.filter(company = company)
	_data = [
		{
			'code': t.decodificar(str(i.code)),
			'description': t.decodificar(str(i.name)),
			'quanty': t.decodificar(str(i.quanty)),
			'initial_inventory':t.decodificar(str(i.initial_inventory)),
			'price': t.decodificar(str(i.price)),
			'category':t.decodificar(str(i.category.name))
		}
		for i in inventory
	]
	return render(request,'reports/inventory.html',{'data':_data})




def Close_The_Box_POS(request):
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = POS.objects.filter(company = company,date = t.codificar(str(date.today())))
	number_invoice = []
	for i in invoice:
		if int(t.decodificar(str(i.number))) not in number_invoice:
			number_invoice.append(int(t.decodificar(str(i.number))))
	_data = []
	for j in number_invoice:
		_i = POS.objects.filter(company = company,date = t.codificar(str(date.today())), number = t.codificar(str(j)))
		subtotal = 0
		tax = 0
		discount = 0
		cost = 0
		total = 0
		for i_ in _i:
			cost += i_.Base_Product_WithOut_Discount()
			subtotal += i_.Base_Product_WithOut_Discount() * float(t.decodificar(str(i_.quanty)))
			tax += i_.Tax_Value()
			total += i_.Totals()
		_data.append({
			'number':j,
			'cost': cost,
			'subtotal':subtotal,
			'discount':discount,
			'tax':tax,
			'totals':total,
			'date':str(date.today())
			})
	return render(request,'reports/close_the_box_pos.html',{'data':_data})



















