from django.db import models
from data.models import Type_Worker,Payroll_Type_Document_Identification,Type_Contract,Municipality
from api.translator import Translator
from company.models import Company
from datetime import date

t = Translator()

class Empleoyee(models.Model):
	documentIdentification = models.TextField(unique=True)
	firstname = models.TextField()
	surname = models.TextField()
	second_surname = models.TextField()
	address = models.TextField()
	type_contract = models.ForeignKey(Type_Contract,on_delete = models.CASCADE)
	payroll_type_document_identification = models.ForeignKey(Payroll_Type_Document_Identification,on_delete = models.CASCADE,default=7)
	type_worker = models.ForeignKey(Type_Worker,on_delete=models.CASCADE,default=1)
	phone = models.TextField()
	email = models.TextField()
	salary = models.TextField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE)
	user = models.TextField()
	passwd = models.TextField()
	block = models.BooleanField(default = False)
	img = models.ImageField(upload_to="Profile-Empleoyee",default = "Profile-Empleoyee/foto.jpg")
	cargo = models.TextField()
	hiring_date = models.TextField(default = date.today())
	type = models.TextField(default = "Empleoyee")

	def __str__(self):
		return t.decodificar(self.firstname)+' '+t.decodificar(self.surname)
