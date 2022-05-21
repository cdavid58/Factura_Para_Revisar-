from django.http import HttpResponse
from django.shortcuts import render
from invoice.models import *
from pos.models import *
from company.models import Company
from api.translator import Translator
from datetime import date,datetime
from date import Count_Days

t = Translator()

def c(request):
	return Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))

def Wallet_Elec(request):
	global c
	wallet = Wallet.objects.filter(company = c(request),paid_out = False).order_by('-pk')
	totals = 0
	number = []
	for i in wallet:
		if t.decodificar(i.invoice.number) not in number:
			number.append(t.decodificar(str(i.invoice.number)))
	_totals = []
	for j in number:	
		_i = Invoice.objects.filter(number = t.codificar(str(j)),company = c(request))
		total = 0
		for x in _i:
			totals += x.Totals()
			total += x.Totals()
		_totals.append(total)
	_data = []
	n = 0
	_mora = []
	for x in wallet:
		pdd = Payment_Form_Invoice.objects.get(invoice = Invoice.objects.filter(number = x.invoice.number).last()).payment_due_date
		_date = pdd.split('-')
		dates = list(map(int, _date))
		days = Count_Days(dates)
		if int(days) < 0:
			_mora.append(int(str(days).replace('-','')))
		else:
			_mora.append(0)
	for i in wallet:
		_data.append(
			{
				'pk':i.pk,
				'code':t.decodificar(str(i.invoice.number)),
				'client':t.decodificar(str(i.invoice.client.name)),
				'date':Payment_Form_Invoice.objects.get(invoice = Invoice.objects.filter(number = i.invoice.number).last()).payment_due_date,
				'price':_totals[n],
				'state':"Pagado" if i.paid_out else "Pendiente",
				'mora':_mora[n]
			}
		)
		n += 1
	if request.is_ajax():
		wallet = Wallet.objects.filter(pk =request.GET.get('number')).last()
		wallet.paid_out = True
		wallet.save()
		History_Invoice(
			wallet = wallet,
			empleoyee = Empleoyee.objects.get(pk = request.session['empleoyee_pk']),
			date = date.today(),
			time = datetime.now()
		).save()
		totals = 0
		number = []
		wallet = Wallet.objects.filter(company = c(request),paid_out = False)
		for i in wallet:
			if t.decodificar(i.invoice.number) not in number:
				number.append(t.decodificar(str(i.invoice.number)))
		for j in number:		
			_i = Invoice.objects.filter(number = t.codificar(str(j)),company = c(request))
			total = 0
			for x in _i:
				totals += x.Totals()
		return HttpResponse(totals)
	return render(request,'Wallet/list_fe.html',{'data':_data,'total':totals})

def Report_Wallet_Elec(request):
	global c
	wallet = Wallet.objects.filter(company = c(request))
	_mora = []
	for x in wallet:
		pdd = Payment_Form_Invoice.objects.get(invoice = Invoice.objects.filter(number = x.invoice.number).last()).payment_due_date
		_date = pdd.split('-')
		dates = list(map(int, _date))
		days = Count_Days(dates)
		if int(days) < 0:
			_mora.append(int(str(days).replace('-','')))
		else:
			_mora.append(0)
	_data = []
	n = 0
	for i in wallet:
		_data.append({
			'pk':i.pk,
			'code':t.decodificar(str(i.invoice.number)),
			'client':t.decodificar(str(i.invoice.client.name)),
			'date':Payment_Form_Invoice.objects.get(invoice = Invoice.objects.filter(number = i.invoice.number).last()).payment_due_date,
			'price':i.invoice.Totals(),
			'state':"Pagado" if i.paid_out else "Pendiente",
			"days_past_due":_mora[n]
		})
		n += 1
	if request.is_ajax():
		wallet = Wallet.objects.filter(pk =request.GET.get('number')).last()
		wallet.paid_out = True
		wallet.save()
		return HttpResponse()
	return render(request,'reports/wallet_fe.html',{'data':_data})

def Electronic_Invoice_Docment_Wallet(request,pk):
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
			'subtotal':round(float(i.Base_Product_WithOut_Discount()),2),
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
		'today': date.today()
	}
	return render(request,'wallet/invoice_fe.html',{
																'invoice':data,'client':client,'company':company,
																'totals':total,'subtotal':subtotal,'tax':tax,'date':_date,'pf':pf,'number_invoice':pk,
																'data_pf':_data_pf
															 }
				)
















def Wallet_Elec_POS(request):
	global c
	wallet = Wallet_POS.objects.filter(company = c(request),paid_out = False).order_by('-pk')
	totals = 0
	number = []
	for i in wallet:
		if t.decodificar(i.pos.number) not in number:
			number.append(t.decodificar(str(i.pos.number)))
	_totals = []
	print(wallet)
	for j in number:	
		_i = POS.objects.filter(number = t.codificar(str(j)),company = c(request))
		total = 0
		for x in _i:
			totals += x.Totals()
			total += x.Totals()
		_totals.append(total)
	_data = []
	n = 0
	_mora = []
	for x in wallet:
		pdd = Payment_Form_Invoice_POS.objects.get(pos = POS.objects.filter(number = x.pos.number).last()).payment_due_date
		_date = pdd.split('-')
		dates = list(map(int, _date))
		days = Count_Days(dates)
		if int(days) < 0:
			_mora.append(int(str(days).replace('-','')))
		else:
			_mora.append(0)

	for i in wallet:
		_data.append(
			{
				'pk':i.pk,
				'code':t.decodificar(str(i.pos.number)),
				'client':t.decodificar(str(i.pos.client.name)),
				'date':Payment_Form_Invoice_POS.objects.get(pos = POS.objects.filter(number = i.pos.number).last()).payment_due_date,
				'price':_totals[n],
				'state':"Pagado" if i.paid_out else "Pendiente",
				'mora':_mora[n]
			}
		)
		n += 1
	if request.is_ajax():
		wallet = Wallet_POS.objects.filter(pk =request.GET.get('number')).last()
		wallet.paid_out = True
		wallet.save()
		History_Invoice_POS(
			wallet = wallet,
			empleoyee = Empleoyee.objects.get(pk = request.session['empleoyee_pk']),
			date = date.today(),
			time = datetime.now()
		).save()
		totals = 0
		number = []
		wallet = Wallet_POS.objects.filter(company = c(request),paid_out = False)
		for i in wallet:
			if t.decodificar(i.pos.number) not in number:
				number.append(t.decodificar(str(i.pos.number)))
		for j in number:		
			_i = POS.objects.filter(number = t.codificar(str(j)),company = c(request))
			for x in _i:
				totals += x.Totals()
		return HttpResponse(totals)

	print(_data)

	return render(request,'wallet_pos/list_pos.html',{'data':_data,'total':totals})























