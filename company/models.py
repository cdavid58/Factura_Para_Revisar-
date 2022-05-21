from django.db import models
from data.models import *
from api.translator import Translator
from datetime import date
from seller.models import Seller


t = Translator()

class Files_Company(models.Model):
	rut = models.FileField(upload_to = "RUT_Company",default="",null=True,blank = True)
	chamber_of_commerce = models.FileField(upload_to = "Chamber_Of_Commerce_Company",default="",null=True,blank = True)
	img_document_identification = models.FileField(upload_to = "Img_Document_Identification",default="",null=True,blank = True)
	name_company = models.TextField(default = "")
	documentIdentification = models.TextField(default = "",unique=True)
	seller = models.ForeignKey(Seller,on_delete = models.CASCADE,default="",null=True,blank=True)
	finished = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False)
	finish_date = models.CharField(max_length=10,default = "")
	cancellation_date = models.CharField(max_length=10,default = "")

	# def __str__(self):
	# 	return t.decodificar(str(self.name_company))


class Company(models.Model):
	documentIdentification = models.TextField(unique = True)
	type_documentI = models.ForeignKey(Type_Document_Identification,on_delete = models.CASCADE)
	type_organization = models.ForeignKey(Type_Organization,on_delete=models.CASCADE)
	type_regime = models.ForeignKey(Type_Regime,on_delete=models.CASCADE)
	business_name = models.TextField()
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
	address = models.TextField()
	phone = models.TextField()
	email = models.TextField()
	certificate_generation_date = models.CharField(max_length=10)
	certificate_expiration_date = models.CharField(max_length=10)
	resolution_generation_date = models.CharField(max_length=10)
	resolution_expiration_date = models.CharField(max_length=10)
	block = models.BooleanField(default = False)
	token = models.TextField()
	user = models.TextField()
	password = models.TextField()
	logo = models.ImageField(upload_to = "Logo_Company",default = "Logo_Company/default.png")
	cod_bars = models.BooleanField(default = True)
	resolution_number = models.TextField(default = "18760000001")
	prefix = models.TextField(default = "SETP")
	license = models.BooleanField(default = False)
	date_register = models.TextField(default=date.today())
	payment_date = models.TextField(default = date.today())
	files_company = models.ForeignKey(Files_Company,on_delete = models.CASCADE,default="",null=True,blank=True)

	def __str__(self):
		return t.decodificar(self.business_name)


class License_Company(models.Model):
	full_license = models.BooleanField(default = False)
	registration_date = models.TextField()
	due_date = models.TextField()
	company = models.ForeignKey(Company,on_delete = models.CASCADE)

	def __str__(self):
		return t.decodificar(self.company.business_name)






