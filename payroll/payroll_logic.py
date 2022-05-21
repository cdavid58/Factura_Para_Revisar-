import pymysql.cursors, pandas as pd, json, requests, numpy as np
from datetime import date
import datetime

class Request:
	def __init__(self):
		self.MyDB = pymysql.connect(host="159.203.170.123",port=3306,user="root",passwd="medellin100",db="payroll",charset='utf8',cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.MyDB.cursor()

	def typeWorker(self,value):
		self.cursor.execute("select id from type_workers where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

	def typeDocument(self,value):
		self.cursor.execute("select id from type_document_identifications where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

	def Municipalities(self,value):
		self.cursor.execute("select id from municipalities where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

	def typeContract(self,value):
		self.cursor.execute("select id from type_contracts where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

	def PaymentMethod(self,value):
		self.cursor.execute("select id from payment_methods where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

	def TypeDisabilities(self,value):
		self.cursor.execute("select id from type_disabilities where name = '"+str(value)+"'")
		return self.cursor.fetchone()['id']

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class Payroll_Calculations:

	def __init__(self,path,worker):
		self.xlsx = path
		self.pages = pd.ExcelFile(path)	
		self.list_pages = self.pages.sheet_names
		self.worker = worker
		self.r = Request()

	def DataPages(self,page):
		data = pd.read_excel(self.xlsx, sheet_name=page)
		return data

	def Worker(self):
		data = self.DataPages(self.list_pages[0])
		identification = data['Cedula Empleado']
		conditional = identification == self.worker
		for i in range(len(data)):			
			if data['Cedula Empleado'].values[i] == self.worker:
				return {
					"type_worker_id": self.r.typeWorker(data['Tipo de Trabajador'].values[i]),
					"sub_type_worker_id": 1,
					"payroll_type_document_identification_id": self.r.typeDocument(data['Tipo de Documento'].values[i]),
					"municipality_id": self.r.Municipalities(data['Municipio'].values[i]),
					"type_contract_id": self.r.typeContract(data['Tipo de Contrato'].values[i]),
					"high_risk_pension": False,
					"identification_number": data['Cedula Empleado'].values[i],
					"surname": data['Primer Apellido'].values[i],
			      "second_surname": "" if 'nan' in str(data['Segundo Apellido'].values[0]) else data['Segundo Apellido'].values[i],
					"first_name": data['Nombre'].values[i],
					"address": data['Domicilio'].values[i],
			      "integral_salarary": False,
			      "salary": data['Sueldo Base'].values[i]
				}

	def PaymentMethod(self):
		data = self.DataPages(self.list_pages[1])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				try:
					if self.r.PaymentMethod(data["Metodo de Pago"].values[i]) == 10:
						return {
							"payment_method_id": self.r.PaymentMethod(data["Metodo de Pago"].values[i]),
						}
					return {
						"payment_method_id": self.r.PaymentMethod(data["Metodo de Pago"].values[i]),
						"bank_name": data['Banco'].values[i],
						"account_type": data['Tipo de Cuenta'].values[i],
						"account_number": data['Numero de Cuenta'].values[i]
					}
				except Exception as e:
					break
		return {'Message':"Por favor verifique el documento excel ya que falta llenar los campos de forma de pago"}

	def Worked_Days(self):
		data = self.DataPages(self.list_pages[0])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				return {"worked_days": data['Dias Trabajdos'].values[i]}


	#################################################################
	#	ACCRUED

	def Salary(self):
		data = self.DataPages(self.list_pages[0])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				return {"salary": data['Sueldo Diario'].values[i]}

	def Transportation_Allowance(self):
		data = self.DataPages(self.list_pages[0])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				return {"transportation_allowance": data['Subsidio de Transport'].values[i]}

	def LogicHours(self,page):
		data = self.DataPages(self.list_pages[page])
		value = data['Cedula Empleado'].dropna()
		values = []
		for i in range(len(value)):
			if data['Cedula Empleado'].values[i] == self.worker:
				values.append({
								"start_time": "2021-03-01T18:00:00",
								"end_time": "2021-03-01T19:00:00",
								"quantity": data['Cantidad'].values[i],
								"percentage": data['Porcentaje'].values[i],
								"payment": data['Total Pago'].values[i]
							}
				      )
		return values if values else 0

	def ExtraHour(self):
		return self.LogicHours(2)

	def ExtraNightTime(self):
		return self.LogicHours(3)

	def ExtraHourNightSurcharge(self):
		return self.LogicHours(4)

	def SundayExtraDaytime(self):
		return self.LogicHours(5)

	def ExtraHourDaytimeSurcharge(self):
		return self.LogicHours(6)

	def SundayExtraNightTime(self):
		return self.LogicHours(7)

	def ExtraHourNightSurchargeSun(self):
		return self.LogicHours(8)


	def LogicVaction(self, page):
		data = self.DataPages(page)
		values = []
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				values.append({
				    "start_date": data['Fecha Inicial'].values[i].astype(str)[:10],
				    "end_date": data['Fecha Final'].values[i].astype(str)[:10],
				    "quantity": data['Cantidad'].values[i],
				    "payment": "{:.2f}".format(data['Total Pago'].values[i])
				})
				return values

	def Vacations(self):
		return self.LogicVaction(9)

	def CompensatedVacationDays(self):
		return self.LogicVaction(10)

	def LogicNonSalaryPremium(self,page):
		data = self.DataPages(self.list_pages[page]).dropna()
		values = []
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				values.append({
	                "quantity": int(data['Cantidad de meses'].values[i]),
	                "payment": "{:.2f}".format(data['Pago Legal'].values[i]),
	                "paymentNS": "{:.2f}".format(data['Pago Extra Legal No Salarial'].values[i])
	            })
				return values

	def ExtraLegalNonSalaryPremium(self):
		return self.LogicNonSalaryPremium(11)


	#############################################################
	#	DEDUCTIONS

	def EPS(self):
		data = self.DataPages(self.list_pages[31])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				return {"eps_type_law_deductions_id": 1,"eps_deduction": data['Pago'].values[i]}

	def Pension(self):
		data = self.DataPages(self.list_pages[31])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				return {"pension_type_law_deductions_id": 5,"pension_deduction": data['Pago'].values[i]}


class Declare_Payroll(Payroll_Calculations):
	def __init__(self,path,worker):
		super().__init__(path,worker)

	def Totals_Accrued(self):
		totals = 0
		totals += float(self.Salary()['salary'])
		totals += float(self.Transportation_Allowance()['transportation_allowance'])
		totals += float(self.ExtraHour()[0]['payment']) if 'nan' not in str(self.ExtraHour()[0]['payment']) else 0
		totals += float(self.ExtraNightTime()[0]['payment']) if 'nan' not in str(self.ExtraNightTime()[0]['payment']) else 0
		totals += float(self.ExtraHourNightSurcharge()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.SundayExtraDaytime()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.ExtraHourDaytimeSurcharge()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.SundayExtraNightTime()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.ExtraHourNightSurchargeSun()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.Vacations()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.CompensatedVacationDays()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.ExtraLegalNonSalaryPremium()[0]['payment']) if 'nan' not in str(self.Salary()['salary']) else 0
		totals += float(self.ExtraLegalNonSalaryPremium()[0]['paymentNS']) if 'nan' not in str(self.Salary()['salary']) else 0
		return totals

	def Totals_Deductions(self):
		totals = 0
		totals += float(self.EPS()['eps_deduction'])
		totals += float(self.Pension()['pension_deduction'])
		
		return totals

	def Preview(self):
		data = self.Data(1)
		data['period'] = self.Period()
		data['worker'] = self.Worker()
		data['payment'] = self.PaymentMethod()
		data['payment_dates'] = {'payment_date':str(date.today())}
		data['accrued'] = self.Accrued()
		data['deductions'] = self.Deductions()

		payload = json.dumps(data,cls=NpEncoder)
		return payload

	def Period(self):
		return {
	        "admision_date": "2021-01-01",
	        "settlement_start_date": "2021-03-01",
	        "settlement_end_date": "2021-03-15",
	        "worked_time": 15,
	        "issue_date": "2021-07-29"
	    }

	def Data(self,consec):
		return {
			"type_document_id": 10,
			"establishment_name": "TORRE SOFTWARE",
			"establishment_address": "CLL 11 NRO 21-73 BRR LA CABAÑA",
			"establishment_phone": "3226563672",
			"establishment_municipality": 600,
			"establishment_email": "alternate_email@alternate.com",
			"foot_note": "Nómina Electrónica elaborada por Evansoft s.a.s",    
			"type_note": 1,
			"worker_code": "41946692",
			"prefix": "NI",
			"consecutive": consec,
			"payroll_period_id": 4,
			"notes": "PRUEBA DE ENVIO DE NOMINA ELECTRONICA"
		}

	def Accrued(self):
		return [
			{
				'worked_days':self.Worked_Days()['worked_days'],
				'salary':self.Salary()['salary'],
				'transportation_allowance':self.Transportation_Allowance()['transportation_allowance'],
				'HEDs':self.ExtraHour(),
				'HENs':self.ExtraNightTime(),
				'HRNs':self.ExtraHourNightSurcharge(),
				'HEDDFs':self.SundayExtraDaytime(),
				'HRDDFs':self.ExtraHourDaytimeSurcharge(),
				'HENDFs':self.SundayExtraNightTime(),
				'HRNDFs':self.ExtraHourNightSurchargeSun(),
				'common_vacation':self.Vacations(),
				'paid_vacation':self.CompensatedVacationDays(),
				'accrued_total':self.Totals_Accrued()
			}
		]

	def Deductions(self):
		return [
			{
				"eps_type_law_deductions_id": self.EPS()['eps_type_law_deductions_id'],
				"eps_deduction": self.EPS()['eps_deduction'],
				"pension_type_law_deductions_id": self.Pension()['pension_type_law_deductions_id'],
				"pension_deduction": self.Pension()['pension_deduction'],
				'deductions_total':self.Totals_Deductions()
			}
		]

# dp = Declare_Payroll(r"C:\Users\David\Downloads\Factura_Para_Revisar\Nomina_formula - copia.xlsx",20302968)
# print(dp.Preview())