from django.contrib import admin
from .models import *

admin.site.register(Invoice)
admin.site.register(Payment_Form_Invoice)
admin.site.register(Consecutive_POS)
admin.site.register(Consecutive_Elec)
admin.site.register(Wallet)
admin.site.register(Consecutive_CreditNote)
admin.site.register(Credit_Note)
admin.site.register(History_Invoice)
