from django.db import models


class Type_Document_Identification(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length = 70)

	def __str__(self):
		return self.name

class Type_Organization(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class Type_Regime(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length = 60)

	def __str__(self):
		return self.name

class Municipality(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name


class Type_Document(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name

class Payment_Form(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name

class Payment_Method(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name


class Type_Worker(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name


class Payroll_Type_Document_Identification(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name

class Type_Contract(models.Model):
	_id = models.IntegerField()
	name = models.CharField(max_length=80)

	def __str__(self):
		return self.name













































