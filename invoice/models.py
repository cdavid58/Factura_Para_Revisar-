from django.db import models
from company.models import *
from client.models import *
from api.translator import Translator
from data.models import *
from empleoyee.models import Empleoyee


t = Translator()

class Consecutive_Elec(models.Model):
	number = models.IntegerField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.decodificar(str(self.company.business_name))

class Consecutive_POS(models.Model):
	number = models.IntegerField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.decodificar(str(self.company.business_name))

class Consecutive_CreditNote(models.Model):
	number = models.IntegerField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.decodificar(str(self.company.business_name))

class Invoice(models.Model):
	number = models.TextField()
	prefix = models.TextField()
	code = models.TextField()
	quanty = models.TextField()
	description = models.TextField()
	price = models.TextField()
	tax = models.TextField()
	notes = models.TextField()
	date = models.TextField()
	ipo = models.TextField()
	discount = models.TextField()
	client = models.ForeignKey(Client,on_delete = models.CASCADE)
	company = models.ForeignKey(Company,on_delete = models.CASCADE)
	type = models.TextField(default = "FE")#FE - POS
	state = models.TextField()
	empleoyee = models.ForeignKey(Empleoyee,on_delete = models.CASCADE)


	def __str__(self):
		return t.decodificar(str(self.number))

	def Base_Product(self):
		return float(t.decodificar(self.price))

	def Tax_Value(self):
		tax =  (float(t.decodificar(str(self.tax))) * float(t.decodificar(str(self.quanty))))
		return round( tax,2)

	def Base_Product_WithOut_Discount(self):
		return round( (self.Base_Product() - ( float(t.decodificar(self.discount)) * 100 )) * float(t.decodificar(str(self.quanty))) )

	def Totals(self):
		return round(self.Base_Product_WithOut_Discount() + self.Tax_Value() + float(t.decodificar(self.ipo)))


class Payment_Form_Invoice(models.Model):
	payment_form_id = models.ForeignKey(Payment_Form,on_delete=models.CASCADE)
	payment_method_id = models.ForeignKey(Payment_Method,on_delete=models.CASCADE)
	payment_due_date = models.TextField()
	duration_measure = models.TextField()
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)


class Wallet(models.Model):
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
	client = models.ForeignKey(Client,on_delete = models.CASCADE)
	price = models.TextField()
	date = models.TextField()
	company = models.ForeignKey(Company,on_delete = models.CASCADE)
	paid_out = models.BooleanField(default = False)
	days_past_due = models.IntegerField(default = 0)

	def __str__(self):
		return t.decodificar(str(self.invoice.number))

class Credit_Note(models.Model):
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
	company = models.ForeignKey(Company,on_delete = models.CASCADE)
	date = models.TextField()

class History_Invoice(models.Model):
	wallet = models.ForeignKey(Wallet,on_delete = models.CASCADE)
	empleoyee = models.ForeignKey(Empleoyee,on_delete = models.CASCADE)
	date = models.TextField()
	time = models.TextField()

	def __str__(self):
		return str(t.decodificar(str(self.empleoyee.firstname)))+ ' ' + str(t.decodificar(str(self.empleoyee.surname)))



