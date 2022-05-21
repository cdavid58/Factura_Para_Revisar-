from inventory.models import Category
from api.translator import Translator
from company.models import Company

t = Translator()

class Create_Category_:
	def __init__(self,data):
		self.data = data

	def Create(self):
		try:
			Category(
				name = t.codificar(str(self.data['name']))
			).save()
			return "Category registration successful"
		except Exception as e:
			return "The category is already registered"
		

