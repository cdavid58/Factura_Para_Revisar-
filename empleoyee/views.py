from django.http import HttpResponse
from django.shortcuts import render,redirect
from api.translator import Translator
from api.SendWelcomeEmpleoye import send_email_empleoyee
from .models import *
import json,queue,threading
from data.models import Type_Document_Identification,Type_Contract

t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def List_Empleoyee(request):
	empleoyee = Empleoyee.objects.filter(company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company']))))
	data = [
		{
			'pk': i.pk,
			'name': t.decodificar(str(i.firstname))+' '+t.decodificar(str(i.surname)),
			'img':i.img.url,
			'post':t.decodificar(str(i.cargo))
		}
		for i in empleoyee
	]
	return render(request,"empleoyee/patients.html",{'empleoyee':data})

def Profile_Empleoyee(request,pk):
	empleoyee = Empleoyee.objects.get(pk = pk)
	data = {
		'pk':empleoyee.pk,
		'img':empleoyee.img.url,
		'name': t.decodificar(str(empleoyee.firstname))+' '+t.decodificar(str(empleoyee.surname)),
		'post':t.decodificar(str(empleoyee.cargo)),
		'email':t.decodificar(str(empleoyee.email)),
		'phone':t.decodificar(str(empleoyee.phone)),
		'address':t.decodificar(str(empleoyee.address)),
		'type':t.decodificar(str(empleoyee.type)),
		'salary': t.decodificar(str(empleoyee.salary))
	}
	return render(request,'empleoyee/patient-profile.html',{'i':data})

def Edit_Empleoyee(request,pk):
	empleoyee = Empleoyee.objects.get(pk = pk)
	request.session['pk_edit_empleoyee'] = pk 
	data = {
		'pk':empleoyee.pk,
		'img':empleoyee.img.url,
		'name': t.decodificar(str(empleoyee.firstname)),
		'last_name':t.decodificar(str(empleoyee.surname)),
		'post':t.decodificar(str(empleoyee.cargo)),
		'email':t.decodificar(str(empleoyee.email)),
		'phone':t.decodificar(str(empleoyee.phone)),
		'address':t.decodificar(str(empleoyee.address)),
		'full_name':t.decodificar(str(empleoyee.firstname))+' '+t.decodificar(str(empleoyee.surname))+' '+str(empleoyee.second_surname),
		'salary': t.decodificar(str(empleoyee.salary)),
		'pwd':t.decodificar(str(empleoyee.passwd)),
		'hiring_date':t.decodificar(str(empleoyee.hiring_date))
	}
	return render(request,'empleoyee/edit-patient.html',{'i':data})

def Delete_Empleoyee(request,pk):
	Empleoyee.objects.get(pk = pk).delete()
	return redirect('List_Empleoyee')

def Information_Basic(request):
	if request.is_ajax():
		empleoyee = Empleoyee.objects.get(pk = request.session['pk_edit_empleoyee'])
		data = request.GET
		empleoyee.firstname = t.codificar(str(data['name']))
		empleoyee.surname = t.codificar(str(data['last_name']))
		empleoyee.hiring_date = t.codificar(str(data['hiring_date']))
		empleoyee.save()
	return HttpResponse(True)

def Information_Persons(request):
	if request.is_ajax():
		data = request.GET
		empleoyee = Empleoyee.objects.get(pk = request.session['pk_edit_empleoyee'])
		empleoyee.email = t.codificar(str(data['email']))
		empleoyee.phone = t.codificar(str(data['phone']))
		empleoyee.passwd = t.codificar(str(data['pwd']))
		empleoyee.save()
		return HttpResponse("")

@storeInQueue
def send_email_empleoyee_back(request,di):
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	empleoyee = Empleoyee.objects.get(company = company,documentIdentification = t.codificar(di))
	send_email_empleoyee(company,empleoyee)


def Add_Empleoyee(request):
	ti = Type_Document_Identification.objects.all()
	tc = Type_Contract.objects.all()
	if request.method == 'POST':
		data = dict(request.POST)
		data = {
		    "documentIdentification":data['documentIdentification'][0],
		    "firstname":data['firstname'][0],
		    "surname":data['surname'][0],
		    "second_surname":"",
		    "address":data['address'][0],
		    "type_contract":data['type_contract'][0],
		    "payroll_type_document_identification":7,
		    "type_worker":3,
		    "phone":data['phone'][0],
		    "email":data['email'][0],
		    "salary":data['salary'][0],
		    "company":request.session['nit_company'],
		    "user":data['user'][0],
		    "post":data['post'][0],
		    "hiring_date":data['hiring_date'][0],
		    "type":data['type'][0],
		    'pwd':data['pwd'][0]
		}
		from api.Create_Empleoyee_ import CreateEmpleoyee
		from django.utils.crypto import get_random_string
		token = get_random_string(length=96)
		c = CreateEmpleoyee(data)
		if c.Create(data['pwd']) == "The employee registered successfully":
			u = threading.Thread(target=send_email_empleoyee_back,args=(request,data['documentIdentification']), name='PDF')
			u.start()

	return render(request,'empleoyee/add-patient.html',{'ti':ti,'tc':tc})






