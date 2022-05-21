from .translator import Translator
from datetime import date
from invoice.models import Invoice,Payment_Form_Invoice
from company.models import Company
from django.shortcuts import render
t = Translator()

class send_invoice_dian:
  def __init__(self,number,nit):
    self.number = number
    self.company = Company.objects.get(documentIdentification = t.codificar(str(nit)))
    self.invoice_ = Invoice.objects
    self.invf = self.invoice_.filter(number = t.codificar(str(number)),company= self.company)
    self.invu = self.invf.last()
    self.fp = Payment_Form_Invoice.objects.get(invoice = self.invu)

  def Customer(self):
    c = self.invu.client
    data = {
      "identification_number": t.decodificar(str(c.identification_number)),
      "dv": t.decodificar(str(c.dv)),
      "name": t.decodificar(str(c.name)),
      "phone": t.decodificar(str(c.phone)),
      "address": t.decodificar(str(c.address)),
      "email": t.decodificar(str(c.email)),
      "merchant_registration": t.decodificar(str(c.merchant_registration)),
      "type_document_identification_id": c.type_documentI.id,
      "type_organization_id": c.type_organization.id,
      "type_liability_id": 7,
      "municipality_id": c.municipality.id,
      "type_regime_id": c.type_regime.id
    }
    return data

  def Invoice_Lines(self):
    data = [
      {
        "unit_measure_id": 70,
        "invoiced_quantity": t.decodificar(str(i.quanty)),
        "line_extension_amount": str(i.Base_Product_WithOut_Discount()),
        "free_of_charge_indicator": False,
        "tax_totals": [
          {
            "tax_id": 1,
            "tax_amount": str(i.Tax_Value()),
            "taxable_amount": str(i.Base_Product_WithOut_Discount()),
            "percent": '19'
          }
        ],
        "description": t.decodificar(str(i.description)),
        "notes": t.decodificar(str(i.notes)),
        "code": t.decodificar(str(i.code)),
        "type_item_identification_id": 4,
        "price_amount": str(i.Totals()),
        "base_quantity": t.decodificar(str(i.quanty))
      }
      for i in self.invf
    ]
    return data

  def Taxs(self):
    list_tax = []
    for i in self.invf:
      if t.decodificar(str(i.tax)) not in list_tax:
        list_tax.append(t.decodificar(str(i.tax)))
    data = []
    values = []
    for j in list_tax:
      _i = self.invoice_.filter(company = self.company,number = t.codificar(str(self.number)),tax = t.codificar(str(j)))
      value_tax = 0
      value_base_product = 0
      for i in _i:
        value_tax += i.Tax_Value()
        value_base_product += i.Base_Product_WithOut_Discount()
      data.append(
        {
          "tax_id": 1,
          "tax_amount": str(value_tax),
          "percent": str(j),
          "taxable_amount": str(value_base_product)
        }
      )
    return data

  def Payment_Form(self):
    data = {
      "payment_form_id": self.fp.payment_form_id.id,
      "payment_method_id": self.fp.payment_method_id.id,
      "payment_due_date": self.fp.payment_due_date,
      "duration_measure": self.fp.duration_measure
    }
    return data

  def Legal_Monetary_Totals(self):
    subtotal = 0
    tax = 0
    total = 0 
    for i in self.invf:
      subtotal += i.Base_Product_WithOut_Discount()
      tax += i.Tax_Value()
      total += i.Totals()
    data = {
      "line_extension_amount": subtotal,
      "tax_exclusive_amount": subtotal,
      "tax_inclusive_amount": tax,
      "payable_amount": total
    }

    return data

  def Send_Electronic_Invoice(self):
    company = self.invu.company
    data = {
      "number": t.decodificar(str(self.invu.number)),
      "type_document_id": 1,
      "date": str(date.today()),
      "Generation_Date":t.decodificar(str(self.invu.date)),
      "time": "04:08:12",
      "resolution_number": str(company.resolution_number),
      "prefix": str(company.prefix),
      "notes": "ESTA ES UNA NOTA DE PRUEBA",
      "disable_confirmation_text": True,
      "establishment_name":  t.decodificar(str(company.business_name)),
      "establishment_address":  t.decodificar(str(company.address)),
      "establishment_phone":  t.decodificar(str(company.phone)),
      "establishment_municipality": company.municipality.id,
      "foot_note": "Factura elaborada por Evansoft - 3004609548"
    }
    import json,requests
    data['customer'] = self.Customer()
    data['payment_form'] = self.Payment_Form()
    data['legal_monetary_totals'] = self.Legal_Monetary_Totals()
    data['tax_totals'] = self.Taxs()
    data['invoice_lines'] = self.Invoice_Lines()
    _data = json.dumps(data)
    for i in self.invf:
      i.state = t.codificar(str("Procesado Correctamente."))
      i.save()
    return _data



