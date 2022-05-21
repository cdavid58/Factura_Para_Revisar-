from django.http import HttpResponse,JsonResponse,FileResponse
from django.shortcuts import render,redirect
from .models import *
from api.translator import Translator
import time, threading, queue,json
from client.models import Client
from inventory.models import Inventory,Discount_Inventory
from django.http.request import QueryDict
from datetime import date
from api.SendInvoiceDian import send_invoice_dian
from date import Count_Days
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from from_number_to_letters import numero_a_letras

t = Translator()
my_queue = queue.Queue()
count = 0

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

@storeInQueue
def Invoice_Data(request):
	print(request.session['nit_company'])
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	_invoice = Invoice.objects.filter(company = company).distinct()
	try:
		import sqlite3
		con = sqlite3.connect('db.sqlite3')
		c = con.cursor()
		c.execute("""
									SELECT DISTINCT i.number,c.name,i.prefix,i.state,i.date from invoice_Invoice as i 
									inner join client_Client as c on c.id = i.client_id
									where i.company_id = """+str(company.pk)+""" order by i.number desc
							""")
		data = c.fetchall()

		_data = [
			{
				'pk':t.decodificar(str(i[0])),
				'number':t.decodificar(str(i[2]))+'-'+t.decodificar(str(i[0])),
				'date':t.decodificar(str(i[4])),
				'client':t.decodificar(str(i[1])),
				'state':t.decodificar(str(i[3]))
			}
			for i in data
		]
		return _data
	except Exception as e:
		print(e)
		return []
	

def List_Invoice(request):
	start = time.time()
	u = threading.Thread(target=Invoice_Data,args=(request,), name='Invoice')
	u.start()
	data = my_queue.get()
	paginator = Paginator(data,100)
	page  = request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	if request.is_ajax():
		_inv = Invoice.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))), number =  t.codificar(str(request.GET.get('pk'))))
		for i in _inv:
			_i = Inventory.objects.get(code =i.code)
			n = int(t.decodificar(str(_i.quanty))) + int(t.decodificar(str(i.quanty)))
			_i.quanty = t.codificar(str(n))
			_i.save()
			i.delete()
		return HttpResponse("")
	return render(request,'fe/list_invoice.html',{'invoice':products})

def Create_Invoice(request):
	company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
	client = Client.objects.filter(company = company)
	inventory = Inventory.objects.filter(company = company)
	if request.is_ajax():
		request.session['client'] = request.GET.get("pk")
		return HttpResponse(request.GET.get("pk"))
	data_client = [
									{'name':t.decodificar(str(i.name)),'code':i.pk}
									for i in client
								]
	data_inventory = [{'code':t.decodificar(str(i.code)),'name':t.decodificar(str(i.name))} for i in inventory]
	pf = Payment_Form.objects.all()
	ce = Consecutive_Elec.objects.get(company = company).number
	if 'payment_form' not in request.session:
		request.session['payment_form'] = 1
	global count
	count = 0
	return render(request,'fe/create_invoice.html',{'client':data_client,'inventory':data_inventory,'cod_bars':company.cod_bars,'pf':pf,'ce':ce})

def a(sms):
	return t.decodificar(str(sms))

def GetProducts(request):
	global count
	if request.is_ajax():
		try:
			_id = Inventory.objects.get(code = t.codificar(str(request.GET.get("pk"))))
			products = [
				{
					'pk':count,
					'code':a(_id.code),
					"name":a(_id.name),
					'cost':_id.Base_Product(),
					'tax':a(_id.tax),
					'discount':0,
					'quanty':a(_id.quanty),
					'tax_value':_id.Tax_Value()
				}
			]
			products = json.dumps(products)
			count += 1
			return HttpResponse(products)
		except Inventory.DoesNotExist:
			return HttpResponse("Error")

def Vence(request):
	if request.is_ajax():
		request.session['date_vence'] = request.GET.get('date')
		request.session['days'] = request.GET.get('days')
		return HttpResponse("")

def Save_Invoice_FE(request):
	if request.is_ajax():
		data = request.GET
		success = False
		for i in data:
			_data = json.loads(i)
			if len(_data) == 0:
				break
			di = Discount_Inventory()
			company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
			consecutive = Consecutive_Elec.objects.get(company = company)
			pm = 0
			price = 0
			for j in _data:
				n = 0
				Invoice(
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
					state = t.codificar(str("Sin enviar a la DIAN")),
					empleoyee = Empleoyee.objects.get(pk = request.session['empleoyee_pk'])
				).save()
				price += float(j['Costo'])
				if n == 0:
					pm = 10 if int(request.session['payment_form']) == 1 else 30
					if pm == 30:
						date_ = request.session['date_vence']
						_date = date_.split('-')
						dates = list(map(int, _date))
						days = Count_Days(dates)
					Payment_Form_Invoice(
						payment_form_id = Payment_Form.objects.get(pk = request.session['payment_form']),
						payment_method_id = Payment_Method.objects.get(_id = pm),
						payment_due_date = date.today() if pm == 10 else request.session['date_vence'],
						duration_measure = 0 if pm == 10 else days,
						invoice = Invoice.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last()
					).save()
				di.Discount(str(j['Código']),int(j['Cantidad']))
			if pm == 30:
				Wallet(
					invoice = Invoice.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last(),
					client = Client.objects.get(pk = request.session['client']),
					price = t.codificar(str(price)),
					date = t.codificar(str(date.today())),
					company = company
				).save()
				n += 1
				request.session['client']
			n = consecutive.number + 1
			consecutive.number = n 
			consecutive.save()
			success = True
		return HttpResponse(success)

def Payment_Forms(request):
	if request.is_ajax():
		print(request.GET.get("pk"))
		request.session['payment_form'] = request.GET.get("pk")
		return HttpResponse(request.session['payment_form'])

def Print_Invoice(request):
	return render(request,'invoice.html')

@storeInQueue
def Sending(request,pk):
	sd = send_invoice_dian(pk,request.session['nit_company'])
	return sd.Send_Electronic_Invoice()

def Send_Dian(request,pk):
	u = threading.Thread(target=Sending,args=(request,pk), name='PDF')
	u.start()
	data = my_queue.get()
	return redirect('List_Invoice')

def Credit_Notes(request,number):
	company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(number = t.codificar(str(number)), company = company)
	print('Hola')
	Credit_Note(
		invoice = invoice.last(),
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
	return redirect('List_Invoice')

def NoteCreditProduct(request):
	if request.is_ajax():
		company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
		inv = Inventory.objects.get(code = t.codificar(str(request.GET.get("pk"))),company = company)
		n = int(t.decodificar(str(inv.quanty))) + int(request.GET.get('quanty'))
		inv.quanty = t.codificar(str(n))
		inv.save()

		print(request.GET.get('consecutive'),'Consecutive')
		_i = Invoice.objects.filter(number = t.codificar(str(request.GET.get('consecutive'))),company = company)
		if len(_i) > 1:
			for j in Invoice.objects.get(number = t.codificar(str(request.GET.get('consecutive'))),code = t.codificar(str(request.GET.get('pk'))),company = company):
				j.delete()
		return HttpResponse(request.GET.get("pk"))
	


def List_Credit_Note(request):
	company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
	cn = Credit_Note.objects.filter(company = company)
	_data = [
			{
				'pk':i.pk,
				'number':t.decodificar(str(i.invoice.prefix))+'-'+t.decodificar(str(i.invoice.number)),
				'date':i.date,
				'client':t.decodificar(str(i.invoice.client.name)),
				'state':t.decodificar(str(i.invoice.state)),
				'invoice':t.decodificar(str(i.invoice.number))
			}
			for i in cn
		]


	return render(request,'fe/credit_note_fe.html',{'invoice':_data})


from jinja2 import Environment, FileSystemLoader
from template.make_pdf import *
import os

def GetPDF(request,pk):
	invoice = Invoice.objects.filter(pk = pk)
	
	env = Environment(loader=FileSystemLoader("template"))
	template = env.get_template("credit_note_sample.html")
	name_doc = "FES-FE"+str(pk)
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
	
	_payment_form = Payment_Form_Invoice.objects.get(invoice = invoice.last())

	data = {
		'name_client':t.decodificar(str(invoice.last().client.name)),
		"email_client":t.decodificar(str(invoice.last().client.email)),
		"address_client":t.decodificar(str(invoice.last().client.address)),
		'phone_client':t.decodificar(str(invoice.last().client.phone)),
		"data": _data,
		'cufe':'a7e53384eb9bb4251a19571450465d51809e0b7046101b87c4faef96b9bc904cf7f90035f444952dfd9f6084eeee2457433f3ade614712f42f80960b2fca43ff',
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
		'payment_form':str(_payment_form.payment_method_id.name).replace('é','e'),
		'duration_measure':_payment_form.payment_due_date,
		'date':t.decodificar(str(i.date)),
		'total_letters': numero_a_letras(subtotal + tax).upper(),
		'type_invoice':"Factura Electonica de venta",
		'consecutive':t.decodificar(str(invoice.last().number))
	}

	html = template.render(data)
	file = open("template/pdfs/"+name_doc+".html",'w')
	file.write(html)
	file.close()
	GeneratePDF(name_doc)
	os.remove('template/pdfs/'+name_doc+'.html')

	return FileResponse(open(name_doc+'.pdf','rb'),content_type='application/pdf')














