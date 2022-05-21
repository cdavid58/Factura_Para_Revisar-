from company.models import *
from data.models import *
from api.translator import Translator
from data.models import *
from invoice.models import Consecutive_Elec,Consecutive_POS,Consecutive_CreditNote
from validate import Validate_Email,Validate_Phone
from seller.models import Seller,Balance
import datetime


t = Translator()

class CreateCompany:

	def __init__(self,data,token,passwd):
		self.data = data
		self.token = token
		self.passwd = passwd

	def Create(self):
		try:			
			if self.Validate()[0]:
				if Validate_Email(self.data['email']):
					if Validate_Phone(self.data['phone']):
						Company(
							documentIdentification = t.codificar(str(self.data['document_identification'])),
							type_documentI = Type_Document_Identification.objects.get(_id = self.data['type_document_identification_id']),
							type_organization = Type_Organization.objects.get(_id = self.data['type_organization_id']),
							type_regime = Type_Regime.objects.get(_id = self.data['type_regime_id']),
							business_name = t.codificar(str(self.data['business_name'])),
							municipality = Municipality.objects.get(_id = self.data['municipality_id']),
							address = t.codificar(str(self.data['address'])),
							phone = t.codificar(str(self.data['phone'])),
							email = t.codificar(str(self.data['email'])),
							certificate_generation_date = self.data['certificate_generation_date'],
							certificate_expiration_date = self.data['certificate_expiration_date'],
							resolution_generation_date = self.data['resolution_generation_date'],
							resolution_expiration_date = self.data['resolution_expiration_date'],
							token = t.codificar(str(self.token)),
							user = t.codificar(str(self.data['user'])),
							password = t.codificar(str(self.passwd)),
							cod_bars = self.data['cod_bars'],
							files_company = Files_Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification']))),
						).save()
						Consecutive_POS(
							number = 1,
							company = Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification'])))
						).save()
						Consecutive_Elec(
							number = 1,
							company = Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification'])))
						).save()
						Consecutive_CreditNote(
							number = 1,
							company = Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification'])))
						).save()
						full_license = True if float(self.data['payment']) == 800000 else False
						now = datetime.datetime.utcnow()
						License_Company(
							full_license = full_license,
							registration_date = t.codificar(str(now)),
							due_date = t.codificar(str(now + datetime.timedelta(days=365) if full_license else datetime.timedelta(days=30))),
							company = Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification'])))
						).save()
						balance = Balance.objects.get(seller = Files_Company.objects.get(documentIdentification = t.codificar(str(self.data['document_identification']))).seller)
						n = float(t.decodificar(balance.amount)) + (float(self.data['payment']) * 0.20 )
						balance.amount = t.codificar(str(n))
						balance.save()
						return "Successfully registered company"
					return "Invalid phone number"
				return "Invalid E-mail"
			return self.Validate()[1]
		except Exception as e:
			print(e)
			return "The company already exists"

	def Validate(self):
		for i in self.data:
			if self.data[i] == "" or self.data[i] == None:
				return (False,"Missing data or wrong data")
		return (True,'Success')
		

