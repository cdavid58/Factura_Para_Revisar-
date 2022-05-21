from company.models import Company
from client.models import Client
from invoice.models import Invoice,Payment_Form_Invoice
from data.models import *
from .translator import Translator
from validate import Validate_Invoice
from empleoyee.models import Empleoyee

t = Translator()

class CreateInvoice:
	def __init__(self,data):
		self.payment = data['payment_form']
		self.invoice = data['invoice_lines']

	def Create_Invoice_Lines(self):
		if not Validate_Invoice(self.invoice)[0]:
			return Validate_Invoice(self.invoice)[1]
		Invoice(
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
			state = t.codificar("Sin enviar a la DIAN"),
			client = Client.objects.get(identification_number = t.codificar(str(self.invoice['client']))),
			company = Company.objects.get(documentIdentification = t.codificar(str(self.invoice['company']))),
			empleoyee = Empleoyee.objects.get(documentIdentification = t.codificar(str(self.invoice['empleoyee'])))
		).save()

	def Create_Payment_Form(self):
		company = Company.objects.get(documentIdentification = t.codificar(str(self.invoice['company'])))
		Payment_Form_Invoice(
			payment_form_id = Payment_Form.objects.get(_id = self.payment['payment_form_id']),
			payment_method_id = Payment_Method.objects.get(_id=self.payment['payment_method_id']),
			payment_due_date = t.codificar(str(self.payment['payment_due_date'])),
			duration_measure = t.codificar(str(self.payment['duration_measure'])),
			invoice = Invoice.objects.filter(company = company,number = t.codificar(str(self.invoice['number']))).last()
		).save()
		return "Electronic invoice created successfully"