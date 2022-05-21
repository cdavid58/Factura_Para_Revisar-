from django.utils.crypto import get_random_string
from seller.models import Seller,Balance
from api.translator import Translator

t = Translator()

class CreateSeller:
	def __init__(self,data):
		self.data = data

	def Register(self):
		try:
			code = get_random_string(length=6)
			Seller(
				code = code,
				name = t.codificar(str(self.data['name'])),
				documentIdentification = t.codificar(str(self.data['documentIdentification'])),
				phone = t.codificar(str(self.data['phone'])),
				email = t.codificar(str(self.data['email']))
			).save()
			Balance(
				seller = Seller.objects.get(documentIdentification = t.codificar(str(self.data['documentIdentification'])))
			).save()
			return "Vendor created successfully, your code is ->"+str(code)
		except Exception as e:
			return "Vendor creation error "+str(e)

			