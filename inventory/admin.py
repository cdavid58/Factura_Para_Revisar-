from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Record)
admin.site.register(SubCategories)