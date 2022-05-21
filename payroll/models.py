from django.db import models
from company.models import Company

class Payroll_Document(models.Model):
   company = models.OneToOneField(Company,on_delete=models.CASCADE,unique=True)
   payroll_document = models.FileField(upload_to = "Payroll_Document")
   month = models.CharField(max_length = 15)
   anio = models.IntegerField(default = 0)