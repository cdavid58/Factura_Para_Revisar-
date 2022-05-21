from .translator import Translator
from company.models import Company
from data.models import Type_Contract, Payroll_Type_Document_Identification, Type_Worker
from empleoyee.models import Empleoyee
from .translator import Translator

t = Translator()

class CreateEmpleoyee:
	def __init__(self,data):
		self.data = data

	def Create(self,passwd):
		try:
			c = Company.objects.get(documentIdentification=t.codificar(str(self.data['company'])))
		except Company.DoesNotExist:
			return "The company is not registered"
		
		Empleoyee(
			documentIdentification = t.codificar(str(self.data['documentIdentification'])),
			firstname = t.codificar(str(self.data['firstname'])),
			surname = t.codificar(str(self.data['surname'])),
			second_surname = t.codificar(str(self.data['second_surname'])),
			address = t.codificar(str(self.data['address'])),
			type_contract = Type_Contract.objects.get(_id = self.data['type_contract']),
			payroll_type_document_identification = Payroll_Type_Document_Identification.objects.get(_id = self.data['payroll_type_document_identification']),
			type_worker = Type_Worker.objects.get(_id = self.data['type_worker']),
			phone = t.codificar(str(self.data['phone'])),
			email = t.codificar(str(self.data['email'])),
			salary = t.codificar(str(self.data['salary'])),
			company = c ,
			user = t.codificar(str(self.data['user'])),
			passwd = t.codificar(str(passwd)),
			cargo = t.codificar(str(self.data['post'])),
			hiring_date = t.codificar(str(self.data['hiring_date'])),
			type = t.codificar(str(self.data['type']))
		).save()
		return "The employee registered successfully"
			


	def Validate(self):
		value = False
		for i in self.data:
			if self.data['second_surname'] != "" or self.data['second_surname'] == "":
				pass
			else:
				if self.data[i] == "" or self.data[i] == None:
					return (False,"Missing data or wrong data")
		return (True,'Success')

