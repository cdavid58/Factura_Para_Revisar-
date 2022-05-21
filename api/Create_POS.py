from company.models import Company
from client.models import Client
from data.models import *
from .translator import Translator
from validate import Validate_Invoice
from pos.models import *

t = Translator()

class CreateInvoicePos:
	def __init__(self,data):
		self.payment = data['payment_form']
		self.invoice = data['invoice_lines']
		self.company = Company.objects.get(documentIdentification = t.codificar(str(self.invoice['company'])))
		self.client = Client.objects.get(identification_number = t.codificar(str(self.invoice['client'])))

	def Create_Invoice_Lines(self):
		if not Validate_Invoice(self.invoice)[0]:
			return Validate_Invoice(self.invoice)[1]
		POS(
			number = t.codificar(str(self.invoice['number'])),
			prefix = t.codificar(str(self.invoice['prefix'])),
			code = t.codificar(str(self.invoice['code'])),
			quanty = t.codificar(str(self.invoice['quanty'])),
			description = t.codificar(str(self.invoice['description'])),
			price = t.codificar(str(self.invoice['price'])),
			tax = t.codificar(str(self.invoice['tax'])),
			notes = t.codificar(str(self.invoice['notes'])),
			date = t.codificar(str(self.invoice['date'])),
			ipo = t.codificar(str(self.invoice['ipo'])),
			discount = t.codificar(str(self.invoice['discount'])),
			client = self.client,
			company = self.company,
			type = "POS"
		).save()

	def Create_Payment_Form(self):
		
		Payment_Form_Invoice_POS(
			payment_form_id = Payment_Form.objects.get(_id = self.payment['payment_form_id']),
			payment_method_id = Payment_Method.objects.get(_id=self.payment['payment_method_id']),
			payment_due_date = t.codificar(str(self.payment['payment_due_date'])),
			duration_measure = t.codificar(str(self.payment['duration_measure'])),
			pos = POS.objects.filter(company = self.company,number = t.codificar(str(self.invoice['number']))).last()
		).save()
		
		if int(self.payment['payment_form_id']) == 2:
			self.Create_Wallet_POS()
		return "POS invoice created successfully"

	def Create_Wallet_POS(self):
		Wallet_POS(
			pos = POS.objects.filter(company = self.company,number = t.codificar(str(self.invoice['number']))).last(),
			client = self.client,
			price = t.codificar(str(self.invoice['price'])),
			date = t.codificar(str(self.invoice['date']))
		).save()