from django.http import HttpResponse
from django.shortcuts import render
from invoice.models import *
from company.models import Company
from client.models import Client
from api.translator import Translator
from datetime import date
from pos.models import *
import time

t = Translator()

def Electronic_Invoice_List(request):
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company)
	return HttpResponse("Bien")

def Electronic_Invoice_Docment(request,pk):
	invoice= Invoice.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))),type = "FE",number = t.codificar(str(pk)))
	_invoice = Invoice.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))),type = "FE",number = t.codificar(str(pk))).last()
	total = 0 
	subtotal = 0
	tax = 0
	for i in invoice:
		tax += round(i.Tax_Value(),2)
		total += round(float(i.Totals()),2)
		subtotal += round(float(i.Base_Product_WithOut_Discount()),2)
	data = [
		{
			'code':t.decodificar(str(i.code)),
			'description':t.decodificar(str(i.description)),
			'quanty':t.decodificar(str(i.quanty)),
			'price':i.Base_Product_WithOut_Discount(),
			'tax':t.decodificar(str(i.tax)),
			'tax_value':i.Tax_Value(),
			'ICO':t.decodificar(str(i.ipo)),
			'discount':0,
			'subtotal':round(float(i.Base_Product_WithOut_Discount()) * float(t.decodificar(str(i.quanty))),2),
			'totals':i.Totals()
		}
		for i in invoice
	]
	client = {
			'name':t.decodificar(str(_invoice.client.name)),
			'address':t.decodificar(str(_invoice.client.address)),
			'phone':t.decodificar(str(_invoice.client.phone)),
			'email':t.decodificar(str(_invoice.client.email))
		}
	company = {
			'name':t.decodificar(str(_invoice.company.business_name)),
			'address':t.decodificar(str(_invoice.company.address)),
			'phone':t.decodificar(str(_invoice.company.phone)),
			'email':t.decodificar(str(_invoice.company.email))
		}

	pf = Payment_Form_Invoice.objects.get(invoice = _invoice)
	_data_pf = {
		'payment_due_date':pf.payment_due_date,
		'duration_measure':pf.duration_measure
	}

	_date = {
		'fg':t.decodificar(str(_invoice.date)),
		'today': date.today(),
		'state':t.decodificar(str(_invoice.state))
	}
	return render(request,'document_payment/invoice_fe.html',{
																'invoice':data,'client':client,'company':company,
																'totals':total,'subtotal':subtotal,'tax':tax,'date':_date,'pf':pf,'number_invoice':pk,
																'data_pf':_data_pf
															 }
				)

def Electronic_Invoice_Docment_POS(request,pk):
	invoice= POS.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))),number = t.codificar(str(pk)))
	_invoice = POS.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))),number = t.codificar(str(pk))).last()
	total = 0 
	subtotal = 0
	tax = 0
	for i in invoice:
		tax += round(i.Tax_Value(),2)
		total += round(float(i.Totals()),2)
		subtotal += round(float(i.Base_Product_WithOut_Discount()),2)
	data = [
		{
			'code':t.decodificar(str(i.code)),
			'description':t.decodificar(str(i.description)),
			'quanty':t.decodificar(str(i.quanty)),
			'price':i.Base_Product_WithOut_Discount(),
			'tax':t.decodificar(str(i.tax)),
			'tax_value':i.Tax_Value(),
			'ICO':t.decodificar(str(i.ipo)),
			'discount':0,
			'subtotal':round(float(i.Base_Product_WithOut_Discount()) * float(t.decodificar(str(i.quanty))),2),
			'totals':i.Totals()
		}
		for i in invoice
	]
	client = {
			'name':t.decodificar(str(_invoice.client.name)),
			'address':t.decodificar(str(_invoice.client.address)),
			'phone':t.decodificar(str(_invoice.client.phone)),
			'email':t.decodificar(str(_invoice.client.email))
		}
	company = {
			'name':t.decodificar(str(_invoice.company.business_name)),
			'address':t.decodificar(str(_invoice.company.address)),
			'phone':t.decodificar(str(_invoice.company.phone)),
			'email':t.decodificar(str(_invoice.company.email))
		}

	pf = Payment_Form_Invoice_POS.objects.get(pos = _invoice)
	_data_pf = {
		'payment_due_date':pf.payment_due_date,
		'duration_measure':pf.duration_measure
	}

	_date = {
		'fg':t.decodificar(str(_invoice.date)),
		'today': date.today(),
		'state':t.decodificar(str(_invoice.state))
	}
	return render(request,'document_payment/invoice_fe.html',{
																'invoice':data,'client':client,'company':company,
																'totals':total,'subtotal':subtotal,'tax':tax,'date':_date,'pf':pf,'number_invoice':pk,
																'data_pf':_data_pf
															 }
				)
