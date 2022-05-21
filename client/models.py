from django.db import models
from api.translator import Translator
from data.models import *
from company.models import *

t = Translator()

class Client(models.Model):
	identification_number = models.TextField(unique=True)
	dv = models.TextField()
	name = models.TextField()
	phone = models.TextField()
	address = models.TextField()
	email = models.TextField()
	merchant_registration = models.TextField()
	type_documentI = models.ForeignKey(Type_Document_Identification,on_delete = models.CASCADE)
	type_organization = models.ForeignKey(Type_Organization,on_delete=models.CASCADE)
	type_regime = models.ForeignKey(Type_Regime,on_delete=models.CASCADE)
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)
	img = models.ImageField(upload_to="Photo_Client",default = "Profile_Client/foto.jpg")

	def __str__(self):
		return t.decodificar(self.name)

