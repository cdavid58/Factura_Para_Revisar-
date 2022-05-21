from django.db import models
from company.models import Company
from api.translator import Translator
from empleoyee.models import Empleoyee

t = Translator()

class Category(models.Model):
	name = models.TextField(default="")

	def __str__(self):
		return t.decodificar(str(self.name))

class SubCategories(models.Model):
	name = models.TextField(default="")
	category = models.ForeignKey(Category,on_delete = models.CASCADE,default="",null=True,blank=True)

	def __str__(self):
		return t.decodificar(str(self.name))	



class Inventory(models.Model):
	code = models.TextField(default="")
	name = models.TextField()
	quanty = models.TextField()
	price = models.TextField()
	tax = models.TextField()
	initial_inventory = models.TextField()
	exhausted = models.BooleanField(default=False)
	subcategories = models.ForeignKey(SubCategories,on_delete = models.CASCADE,default="",null=True,blank=True)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.decodificar(str(self.name))

	def Base_Product(self):
		return round(float(t.decodificar(str(self.price))) / (1 + (float( t.decodificar(str(self.tax)) )) / 100),2)

	def Tax_Value(self):
		return round( float(t.decodificar(self.price))  - self.Base_Product(),2)


class Record(models.Model):
	code = models.TextField()
	quanty = models.TextField()
	price = models.TextField()
	tax = models.TextField()
	date = models.TextField()
	time = models.TextField()
	empleoyee = models.ForeignKey(Empleoyee,on_delete=models.CASCADE)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)


class Discount_Inventory:
	def __str__(self):
		pass

	def Discount(self,cod,quanty):
		print(cod)
		self.i = Inventory.objects.get(code = t.codificar(str(cod)))
		if int(t.decodificar(str(self.i.quanty))) >= quanty:
			less = int(t.decodificar(str(self.i.quanty))) - quanty
			self.i.quanty = t.codificar(str(less))
			self.i.save()
		if int(t.decodificar(str(self.i.quanty))) == 0:
			self.i.exhausted = True
			self.i.save()




