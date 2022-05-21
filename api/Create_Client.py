from company.models import *
from data.models import *
from .translator import Translator
from client.models import Client
from validate import *

t = Translator()

class CreateClient:
	def __init__(self,data):
		self.data = data 

	def Create(self):
		try:
			if not Validate_Email(self.data['email']):
				return "The email is invalid"
			if not Validate_Phone(self.data['phone']):
				return "The phone is invalid"
				
			Client(
				identification_number = t.codificar(str(self.data['identification_number'])),
				dv = t.codificar(str(self.data['dv'])),
				name = t.codificar(str(self.data['name'])),
				phone = t.codificar(str(self.data['phone'])),
				address = t.codificar(str(self.data['address'])),
				email = t.codificar(str(self.data['email'])),
				merchant_registration = t.codificar(str(self.data['merchant_registration'])),
				type_documentI = Type_Document_Identification.objects.get(_id = self.data['type_document_identification_id']),
				type_organization = Type_Organization.objects.get(_id = self.data['type_organization_id']),
				type_regime = Type_Regime.objects.get(_id = self.data['type_regime_id']),
				municipality = Municipality.objects.get(_id = self.data['municipality_id']),
				company = Company.objects.get(documentIdentification=t.codificar(str(self.data['company'])))
			).save()
			return "Successfully registered customer"
		except ValueError as v:
			return "The customer data is not valid"
		except Exception as e:
			print(e)
			return "The client is already registered"
		






