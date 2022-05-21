from django.http import HttpResponse,FileResponse
from django.shortcuts import render
from api.translator import Translator
import time, threading, queue,json
from company.models import Company
from client.models import Client
from .models import *
from inventory.models import Inventory
from data.models import *
from invoice.models import Consecutive_POS
from datetime import date
from date import Count_Days
from inventory.models import Inventory,Discount_Inventory
from from_number_to_letters import numero_a_letras

t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def Create_POS(request):
	company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
	client = Client.objects.filter(company = company)
	inventory = Inventory.objects.filter(company = company)
	request.session['client'] = Client.objects.get(name = t.codificar('CLIENTE GENERAL')).pk
	if request.is_ajax():
		request.session['client'] = request.GET.get("pk")
		return HttpResponse(request.GET.get("pk"))
	data_client = [{'name':t.decodificar(str(i.name)),'code':i.pk}for i in client]
	data_inventory = [{'code':t.decodificar(str(i.code)),'name':t.decodificar(str(i.name))} for i in inventory]
	pf = Payment_Form.objects.all()
	ce = Consecutive_POS.objects.get(company = company).number
	return render(request,'pos/create_invoice.html',{'client':data_client,'inventory':data_inventory,'cod_bars':company.cod_bars,'pf':pf,'ce':ce})

def a(sms):
	return t.decodificar(str(sms))

def GetProducts_POS(request):
	if request.is_ajax():
		try:
			_id = Inventory.objects.get(code = t.codificar(str(request.GET.get("pk"))))
			products = [{'code':a(_id.code),"name":a(_id.name),'cost':_id.Base_Product(),'tax':a(_id.tax),'discount':0}]
			products = json.dumps(products)
			return HttpResponse(products)
		except Inventory.DoesNotExist:
			return HttpResponse("Error")

def Vence_Pos(request):
	if request.is_ajax():
		print(request.GET.get('date'))
		request.session['date_vence'] = request.GET.get('date')
		request.session['days'] = request.GET.get('days')
		return HttpResponse("")

def Save_Invoice_Pos(request):
	if request.is_ajax():
		data = request.GET
		try:
			success = False
			for i in data:
				_data = json.loads(i)
				if len(_data) == 0:
					break
				di = Discount_Inventory()
				company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
				consecutive = Consecutive_POS.objects.get(company = company)
				pm = 0
				price = 0
				for j in _data:
					n = 0
					POS(
						number = t.codificar(str(consecutive.number)),
						prefix = t.codificar("FE"),
						code = t.codificar(str(j['Código'])),
						quanty = t.codificar(str(j['Cantidad'])),
						description = t.codificar(str(j['Descripción'])),
						price = t.codificar(str(j['Costo'])),
						tax = t.codificar(str(j['Iva'])),
						notes = t.codificar(str("No Hay")),
						date = t.codificar(str(date.today())),
						ipo = t.codificar(str(0)),
						discount = t.codificar(str(j['Desc.'])),
						client = Client.objects.get(pk = request.session['client']),
						company = company,
						empleoyee = Empleoyee.objects.get(pk=request.session['empleoyee_pk']),
						state = t.codificar("Facturado al contado") if int(request.session['payment_form']) == 1 else t.codificar("Facturado a credito")
					).save()
					price += float(j['Costo'])
					if n == 0:
						pm = 10 if int(request.session['payment_form']) == 1 else 30
						if pm == 30:
							date_ = request.session['date_vence']
							_date = date_.split('-')
							dates = list(map(int, _date))
							days = Count_Days(dates)
						print(pm)
						Payment_Form_Invoice_POS(
							payment_form_id = Payment_Form.objects.get(pk = request.session['payment_form']),
							payment_method_id = Payment_Method.objects.get(_id = pm),
							payment_due_date = date.today() if pm == 10 else request.session['date_vence'],
							duration_measure = 0 if pm == 10 else days,
							pos = POS.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last()
						).save()
				di.Discount(str(j['Código']),int(j['Cantidad']))
				if pm == 30:
					Wallet_POS(
						pos = POS.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last(),
						client = Client.objects.get(pk = request.session['client']),
						price = t.codificar(str(price)),
						date = t.codificar(str(date.today())),
						company = company,
					).save()
					n += 1
					request.session['client']
				n = consecutive.number + 1
				consecutive.number = n 
				consecutive.save()
				success = True
			return HttpResponse(success)
		except Exception as e:
			print(e)
			return HttpResponse(False)

def Payment_Forms_POS(request):
	if request.is_ajax():
		print(request.GET.get("pk"))
		request.session['payment_form'] = request.GET.get("pk")
		return HttpResponse(request.session['payment_form'])

@storeInQueue
def Invoice_Data(request):
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	_invoice = POS.objects.filter(company = company).values_list('number', flat=True).distinct()
	data = []
	for j in _invoice.order_by('-pk'):
		if j not in data:
			data.append(j)
	_data = []
	for i in data:
		_i = POS.objects.filter(company=company,number = i).last()
		_data.append(
				{
				'pk': t.decodificar(str(_i.number)),
				'number':t.decodificar(str(_i.prefix))+'-'+t.decodificar(str(_i.number)),
				'date': t.decodificar(str(_i.date)),
				'client':t.decodificar(str(_i.client.name)),
				'state':t.decodificar(str(_i.state)),
				'totals':round(_i.Totals())
			}
		)
	return _data

def List_Invoice_POS(request):	
	u = threading.Thread(target=Invoice_Data,args=(request,), name='PDF')
	u.start()
	data = my_queue.get()
	return render(request,'pos/list_invoice.html',{'invoice':data})

def Print_Invoice(request):
	return render(request,'invoice.html')


def Credit_Notes(request):
	if request.is_ajax:
		company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
		invoice = POS.objects.filter(number = t.codificar(str(request.GET.get("pk"))), company = company)
		print(invoice)
		Credit_Note_POS(
			pos = invoice.last(),
			company = company,
			date = date.today()
		).save()
		for i in invoice:
			inv = Inventory.objects.get(code = i.code,company = company)
			n = int(t.decodificar(str(inv.quanty))) + int(t.decodificar(str(i.quanty)))
			inv.quanty = t.codificar(str(n))
			inv.save()
			if int(t.decodificar(str(inv.quanty))) > 0:
				inv.exhausted = False
				inv.save()
			i.state = t.codificar(str("Se aplico nota crédito"))
			i.save()
		return HttpResponse(1)


def List_Credit_Note_POS(request):
	company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
	cn = Credit_Note_POS.objects.filter(company = company)
	_data = [
			{
				'pk':i.pk,
				'number':t.decodificar(str(i.pos.prefix))+'-'+t.decodificar(str(i.pos.number)),
				'date':i.date,
				'client':t.decodificar(str(i.pos.client.name)),
				'state':t.decodificar(str(i.pos.state)),
				'invoice':t.decodificar(str(i.pos.number))
			}
			for i in cn
		]


	return render(request,'pos/credit_note_pos.html',{'invoice':_data})





from jinja2 import Environment, FileSystemLoader
from template.make_pdf import *
import os

def GetPDF_POS(request,pk):
	invoice = POS.objects.filter(pk = pk)
	
	env = Environment(loader=FileSystemLoader("template"))
	template = env.get_template("credit_note_sample.html")
	name_doc = "FES-POS"+str(pk)
	_data = [
		{
			'code':t.decodificar(str(i.code)),
			"name":t.decodificar(str(i.description)),
			"quanty":t.decodificar(str(i.quanty)),
			"price":t.decodificar(str(i.price)),
			'tax_value':i.Tax_Value(),
			'ico':t.decodificar(str(i.ipo)),
			'discount':i.Totals_Discount(),
			'totals':i.Base_Product_WithOut_Discount()
		}
		for i in invoice
	]
	subtotal = 0
	tax = 0
	for i in invoice:
		subtotal += i.Base_Product_WithOut_Discount()
		tax += i.Tax_Value()
	
	_payment_form = Payment_Form_Invoice_POS.objects.get(pos = invoice.last())

	data = {
		'name_client':t.decodificar(str(invoice.last().client.name)),
		"email_client":t.decodificar(str(invoice.last().client.email)),
		"address_client":t.decodificar(str(invoice.last().client.address)),
		'phone_client':t.decodificar(str(invoice.last().client.phone)),
		"data": _data,
		'subtotal_invoice':subtotal,
		'tax':tax,
		'total_invoice':subtotal + tax,
		'title':name_doc,
		'name_company':t.decodificar(str(invoice.last().empleoyee.company.business_name)),
		'address_company':t.decodificar(str(invoice.last().empleoyee.company.address)),
		'email_company':t.decodificar(str(invoice.last().empleoyee.company.email)),
		'phone_company':t.decodificar(str(invoice.last().empleoyee.company.phone)),
		'resolution_number':invoice.last().empleoyee.company.resolution_number,
		'type_organization':invoice.last().empleoyee.company.type_organization.name,
		'payment_form':_payment_form.payment_method_id.name,
		'duration_measure':_payment_form.payment_due_date,
		'date':t.decodificar(str(i.date)),
		'total_letters': numero_a_letras(subtotal + tax).upper(),
		'type_invoice':"Factura POS"
	}

	html = template.render(data)
	file = open("template/pdfs/"+name_doc+".html",'w')
	file.write(html)
	file.close()
	GeneratePDF(name_doc)
	os.remove('template/pdfs/'+name_doc+'.html')

	return FileResponse(open(name_doc+'.pdf','rb'),content_type='application/pdf')





