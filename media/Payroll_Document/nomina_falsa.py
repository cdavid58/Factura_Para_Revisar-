import pymysql.cursors, pandas as pd, json, requests
from datetime import date
import numpy as np

class Request:
	def __init__(self):
		self.MyDB = pymysql.connect(host="159.203.170.123",port=3306,user="root",passwd="medellin100",db="apidian2022",charset='utf8',cursorclass=pymysql.cursors.DictCursor)
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


class PayRollCustom:


	def __init__(self,path,worker):
		self.xlsx = path
		self.pages = pd.ExcelFile(path)	
		self.list_pages = self.pages.sheet_names
		self.worker = worker
		self.r = Request()
		self.totalAccrued = 0
		self.TotalsDeductions = 0

	def Validate(self,page):
		data = self.DataPages(self.list_pages[page])
		for i in range(len(data)):
			if self.worker in data['Cedula Empleado'].values:
				return True
		return False

	def DataPages(self,page):
		data = pd.read_excel(self.xlsx, sheet_name=page)
		return data

	def FormatDate(self,date):
		value = pd.to_datetime(date, format='%Y%m%d')
		return value

	def FormatHour(self,hour):
		value = pd.to_datetime(hour, format='%H:%M:%S')
		return value

	def LogicHours(self,page):
		data = self.DataPages(page)
		identification = data['Cedula Empleado']
		value = data['Cedula Empleado'].dropna()
		values = []
		for i in range(len(value)):
			if self.Validate(page):
				if data['Cedula Empleado'].values[i] == self.worker:
					date = self.FormatDate(data['Fecha'].values[i])
					date = str(date).replace(' ','T')
					hi = str(self.FormatHour(data['Hora Inicial'].values[i]))[-8:]
					hf = str(self.FormatHour(data['Hora Final'].values[i]))[-8:]
					values.append(
						{
					              "start_time": "2021-11-30T17:00:00",
					              "end_time": "2021-11-30T19:00:00",
					              "quantity": int(data['Cantidad'].values[i]),
					              "percentage": 1,
					              "payment": "{:.2f}".format(data['Total Pago'].values[i])
					          }
					      )
					self.totalAccrued += float(data['Total Pago'].values[i])
					break
		return values if values else 0


	def LogicVaction(self, page):
		print(page)
		data = self.DataPages(page)
		values = []
		for i in range(len(data)):
			if self.Validate(page):
				start_date = str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10]
				end_date = str(self.FormatDate(data['Fecha Final'].values[i]))[:10]
				self.totalAccrued += float(data['Total Pago'].values[i])
				values.append({
				    "start_date": start_date,
				    "end_date": end_date,
				    "quantity": int(data['Cantidad'].values[i]),
				    "payment": "{:.2f}".format(data['Total Pago'].values[i])
				})
			print(values)

	def LogicNonSalaryPremium(self,page):
		data = self.DataPages(self.list_pages[page]).dropna()
		values = []
		print(self.worker)
		for i in range(len(data)):
			if self.Validate(page):
				if data['Cedula Empleado'].values[i] == self.worker:
					self.totalAccrued += float(data['Pago Legal'].values[i])
					self.totalAccrued += float(data['Pago Extra Legal No Salarial'].values[i])
					values.append({
		                "quantity": int(data['Cantidad'].values[i]),
		                "payment": "{:.2f}".format(data['Pago Legal'].values[i]),
		                "paymentNS": "{:.2f}".format(data['Pago Extra Legal No Salarial'].values[i])
		            })

		return values if values else 0

	def Worker(self):
		data = self.DataPages(self.list_pages[0])
		identification = data['Cedula Empleado']
		conditional = identification == self.worker
		# value = data['Cedula Empleado'].dropna()
		for i in range(len(data)):			
			if data['Cedula Empleado'].values[i] == self.worker:
				values = {
					"type_worker_id": self.r.typeWorker(data['Tipo de Trabajador'].values[i]),
					"sub_type_worker_id": 1,
					"payroll_type_document_identification_id": self.r.typeDocument(data['Tipo de Documento'].values[i]),
					"municipality_id": self.r.Municipalities(data['Municipio'].values[i]),
					"type_contract_id": self.r.typeContract(data['Tipo de Contrato'].values[i]),
					"high_risk_pension": False,
					"identification_number": self.worker,
					"surname": data['Primer Apellido'].values[i],
			        "second_surname": "",
					"first_name": data['Nombre'].values[i],
					"address": data['Domicilio'].values[i],
			        "integral_salarary": False,
			        "salary": "{:.2f}".format(data['Salario Mensual'].values[i])
				}
				# self.totalAccrued += float(data['Salario'].values[i])
				return values if values else 0

	def SalaryMensual(self):
		data = self.DataPages(self.list_pages[0])
		identification = data['Cedula Empleado']
		conditional = identification == self.worker
		for i in range(len(data)):
			self.totalAccrued += float(data['Salario'].values[i])
			if data['Cedula Empleado'].values[i] == self.worker:
				return "{:.2f}".format(data['Salario'].values[i])


	def PaymentDates(self):
		data = [
			{
			    "payment_date": str(date.today().year)+"-"+str(date.today().month)+"-30"
			}
		]
		return data

	def OtherValues(self):
		data = self.DataPages(self.list_pages[0])
		for i in range(len(data)):			
			if data['Cedula Empleado'].values[i] == self.worker:
				# self.totalAccrued += float(data['Subsidio de Transport'].values[i])
				values = data['Dias Trabajdos'].values[i]
				transport = "{:.2f}".format(data['Subsidio de Transport'].values[i])
				self.totalAccrued += float(data['Subsidio de Transport'].values[i])
				return (values,transport)

	def PaymentMethod(self):
		data = self.DataPages(self.list_pages[1])
		for i in range(len(data)):
			if data['Cedula Empleado'].values[i] == self.worker:
				if self.r.PaymentMethod(data["Metodo de Pago"].values[i]) == 10:
					print('Efectivo')
					return {
						"payment_method_id": 10
					}
				return {
					"payment_method_id": self.r.PaymentMethod(data["Metodo de Pago"].values[i]),
			        "bank_name": data["Banco"].values[i],
			        "account_type": data["Tipo de Cuenta"].values[i],
			        "account_number": str(int(data["Numero de Cuenta"].values[i]))
				}
				# return values

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

	def Vacations(self):
		return self.LogicVaction(9)

	def CompensatedVacationDays(self):
		return self.LogicVaction(10)

	def ExtraLegalNonSalaryPremium(self):
		return self.LogicNonSalaryPremium(11)

	def ServiceBonus(self):
		data = self.DataPages(self.list_pages[12])
		values = []
		for i in range(len(data)):
			if self.Validate(12):
				if data['Cedula Empleado'].values[i] == self.worker:
					self.totalAccrued += float(data['Tasa de Intereses'].values[i])
					values.append(
						{
							"payment": data['Pago Censatias'].values[i],
	                		"percentage": data['Porcentaje'].values[i],
						    "interest_payment": data['Tasa de Intereses'].values[i]
						}
					)
					break
		return values if values else 0


	def WorkDisabilities(self):
		data = self.DataPages(self.list_pages[13])
		values = []
		for i in range(len(data)):
			if self.Validate(13):
				self.totalAccrued += float(data['Pago Total'].values[i])
				values.append({
					"start_date": str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10],
					"end_date": str(self.FormatDate(data['Fecha Final'].values[i]))[:10],
					"type": self.r.TypeDisabilities(data['Tipo'].values[i]),
					"quantity": int(data['Cantidad'].values[i]),
					"payment": "{:.2f}".format(data['Pago Total'].values[i])
				})
				break
		return values if values else 0
	

	def MaternityLeave(self):
		data = self.DataPages(self.list_pages[14])
		values = []
		for i in range(len(data)):
			if self.Validate(14):
				self.totalAccrued += float(data['Pago Total'].values[i])
				values.append({
					"start_date": str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10],
					"end_date": str(self.FormatDate(data['Fecha Final'].values[i]))[:10],
					"quantity": int(data['Cantidad'].values[i]),
					"payment": "{:.2f}".format(data['Pago Total'].values[i])
				})
		return values if values else 0

	def PaidLeave(self):
		data = self.DataPages(self.list_pages[15]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(15):
				self.totalAccrued += float(data['Pago Total'].values[i])
				values.append({
					"start_date": str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10],
					"end_date": str(self.FormatDate(data['Fecha Final'].values[i]))[:10],
					"quantity": int(data['Cantidad'].values[i]),
					"payment": "{:.2f}".format(data['Pago Total'].values[i])
				})
		return values if values else 0


	def PaidNotLeave(self):
		data = self.DataPages(self.list_pages[16]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(16):
				self.totalAccrued += float(data['Pago Total'].values[i])
				values.append({
					"start_date": str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10],
					"end_date": str(self.FormatDate(data['Fecha Final'].values[i]))[:10],
					"quantity": int(data['Cantidad'].values[i]),
					"payment": "{:.2f}".format(data['Pago Total'].values[i])
				})
		return values if values else 0

	def BonusSocial(self):
		data = self.DataPages(self.list_pages[17]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(17):
				if data['Cedula Empleado'].values[i] == self.worker:
					self.totalAccrued += float(data['Bono Salario'].values[i])
					values.append({
						"salary_bonus": "{:.2f}".format(data['Bono Salario'].values[i])
					})
					break
		return values if values else 0


	def SalaryAssistant(self):
		data = self.DataPages(self.list_pages[18]).dropna()
		values = []
		for i in range(len(data)):
			self.totalAccrued += float(data['Auxilio Salario'].values[i])
			self.totalAccrued += float(data['Auxilio no Salario'].values[i])
			if self.Validate(18):
				values.append({
					"salary_assistance": "{:.2f}".format(data['Auxilio Salario'].values[i]),
					"non_salary_assistance": "{:.2f}".format(data['Auxilio no Salario'].values[i])
				})
		return values if values else 0


	def LegalStrike(self):
		data = self.DataPages(self.list_pages[19]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(19):
				self.totalAccrued += float(data['Pago Total'].values[i])
				values.append({
					"start_date": str(self.FormatDate(data['Fecha Inicial'].values[i]))[:10],
					"end_date": str(self.FormatDate(data['Fecha Final'].values[i]))[:10],
					"quantity": int(data['Cantidad'].values[i]),
					"payment": "{:.2f}".format(data['Pago Total'].values[i])
				})
		return values if values else 0


	def OtherConcepts(self):
		data = self.DataPages(self.list_pages[20]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(20):
				self.totalAccrued += float(data['Salarial'].values[i])
				self.totalAccrued += float(data['No Salarial'].values[i])
				values.append({
					"salary_concept": "{:.2f}".format(data['Salarial'].values[i]),
					"non_salary_concept": "{:.2f}".format(data['No Salarial'].values[i]),
					"description_concept": data['Concepto'].values[i]
				})
		return values if values else 0



	def Compensations(self):
		data = self.DataPages(self.list_pages[21]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(21):
				self.totalAccrued += float(data['Compensacion Ordinaria'].values[i])
				self.totalAccrued += float(data['Compensacion ExtraOrdinaria'].values[i])
				values.append({
					"ordinary_compensation": "{:.2f}".format(data['Compensacion Ordinaria'].values[i]),
					"extraordinary_compensation": "{:.2f}".format(data['Compensacion ExtraOrdinaria'].values[i])
				})
		return values if values else 0


	def EpctvBonuses(self):
		data = self.DataPages(self.list_pages[22]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(22):
				self.totalAccrued += float(data['Pago Salarial'].values[i])
				self.totalAccrued += float(data['Pago No Salarial'].values[i])
				self.totalAccrued += float(data['Pago Salarial Alimentacion'].values[i])
				self.totalAccrued += float(data['Pago No Salarial Alimentacion'].values[i])
				values.append({
					"paymentS": "{:.2f}".format(data['Pago Salarial'].values[i]),
					"paymentNS": "{:.2f}".format(data['Pago No Salarial'].values[i]),
					"salary_food_payment": "{:.2f}".format(data['Pago Salarial Alimentacion'].values[i]),
					"non_salary_food_payment": "{:.2f}".format(data['Pago No Salarial Alimentacion'].values[i])
				})
		return values if values else 0


	def Commissions(self):
		data = self.DataPages(self.list_pages[23]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(23):
				self.totalAccrued += float(data['Comision'].values[i])
				values.append({
					"commission": "{:.2f}".format(data['Comision'].values[i])
				})
		return values if values else 0



	def ThirdPartyPayments(self):
		data = self.DataPages(self.list_pages[24]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(24):
				self.totalAccrued += float(data['Pago Tercera Partes'].values[i])
				values.append({
                "third_party_payment": "{:.2f}".format(data['Pago Tercera Partes'].values[i])
            })
		return values if values else 0



	def Advances(self):
		data = self.DataPages(self.list_pages[25]).dropna()
		values = []
		for i in range(len(data)):
			self.totalAccrued += float(data['Avances'].values[i])
			if self.Validate(25):
				values.append({
	                "advance": "{:.2f}".format(data['Avances'].values[i])
	            })
		return values if values else 0



	def Endowment(self):
		data = self.DataPages(self.list_pages[26]).dropna()
		print(data)
		for i in range(len(data)):
			if self.Validate(26):
				return {'endowment':"{:.2f}".format(data['Avances'].values[i])}
		return 0


	def SustenanceSupport(self):
		data = self.DataPages(self.list_pages[27]).dropna()
		for i in range(len(data)):
			if self.Validate(27):
				self.totalAccrued += float(data['Pago'].values[i])
				return "{:.2f}".format(data['Pago'].values[i]) if data['Pago'].values[i] != "null" else 0
		return 0

	def Telecommuting(self):
		data = self.DataPages(self.list_pages[28]).dropna()
		for i in range(len(data)):
			if self.Validate(28):
				self.totalAccrued += float(data['Pago'].values[i])
				return "{:.2f}".format(data['Pago'].values[i]) if data['Pago'].values[i] != "null" else 0
		return 0


	def WithdrawalBonus(self):
		data = self.DataPages(self.list_pages[29]).dropna()
		for i in range(len(data)):
			if self.Validate(29):
				if self.worker == data['Cedula Empleado'].values[i]:
					self.totalAccrued += float(data['Pago'].values[i])
					return "{:.2f}".format(data['Pago'].values[i]) if data['Pago'].values[i] != "null" else 0
		return 0

	def Compensation(self):
		data = self.DataPages(self.list_pages[30]).dropna()
		for i in range(len(data)):
			if self.Validate(30):
				self.totalAccrued += float(data['Pago'].values[i])
				return "{:.2f}".format(data['Pago'].values[i]) if data['Pago'].values[i] != "null" else 0
		return 0

	def AccruedTotal(self):
		return str(float(self.totalAccrued))





	#################################################################
	# DEDUCTIONS

	def EPSDeduction(self):
		data = self.DataPages(self.list_pages[31]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(31):
				if data['Cedula Empleado'].values[i] == self.worker:
					self.TotalsDeductions += float(data['Pago'].values[i])
					return "{:.2f}".format(data['Pago'].values[i])


	def PensionDeduction(self):
		data = self.DataPages(self.list_pages[32]).dropna()
		values = []
		n = 0
		for i in range(len(data)):
			if self.Validate(32):
				if data['Cedula Empleado'].values[n] == self.worker:
					self.TotalsDeductions += float(data['Pago'].values[n])
					return "{:.2f}".format(data['Pago'].values[n])
			n+=1
		return 1


	def LaborUnion(self):
		data = self.DataPages(self.list_pages[33]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(33):
				self.TotalsDeductions += float(data['Pago'].values[i])
				values.append({
					"percentage": data['Porcentaje'].values[i],
					"deduction": "{:.2f}".format(data['Pago'].values[i])
				})
				return values
		return 0

	def Sanctions(self):
		data = self.DataPages(self.list_pages[34]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(34):
				self.TotalsDeductions += float(data['Publica'].values[i])
				self.TotalsDeductions += float(data['Privada'].values[i])
				values.append({
					"public_sanction": "{:.2f}".format(data['Publica'].values[i]),
					"private_sanction": "{:.2f}".format(data['Privada'].values[i])
				})
				return values
		return 0

	def Orders(self):
		data = self.DataPages(self.list_pages[35]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(35):
				self.TotalsDeductions += float(data['Valor'].values[i])
				values.append({
					"description": data['Descripcion'].values[i],
					"deduction": "{:.2f}".format(data['Valor'].values[i])
				})
				return values
		return 0

	def ThirdPartyPaymentsD(self):
		data = self.DataPages(self.list_pages[36]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(36):
				self.TotalsDeductions += float(data['Valor'].values[i])
				values.append({
                	"third_party_payment": "{:.2f}".format(data['Valor'].values[i])
            	})
				return values
		return 0

	def AdvancesD(self):
		data = self.DataPages(self.list_pages[37]).dropna()
		values = []
		for i in range(len(data)):
			self.TotalsDeductions += float(data['Valor'].values[i])
			if self.Validate(37):
				values.append({
                	"advance": "{:.2f}".format(data['Valor'].values[i])
            	})
				return values
		return 0

	def OtherDeductions(self):
		data = self.DataPages(self.list_pages[38]).dropna()
		values = []
		for i in range(len(data)):
			if self.Validate(38):
				if data['Cedula Empleado'].values[i] == self.worker:
					self.TotalsDeductions += float(data['Valor'].values[i])
					values.append({
	                	"other_deduction": "{:.2f}".format(data['Valor'].values[i])
	            	})
					return values
		return 0

	def VoluntaryPension(self):
		data = self.DataPages(self.list_pages[39]).dropna()
		for i in range(len(data)):
			if self.Validate(39):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def WithholdingAtSource(self):
		data = self.DataPages(self.list_pages[40]).dropna()
		for i in range(len(data)):
			if self.Validate(40):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def AFC(self):
		data = self.DataPages(self.list_pages[41]).dropna()
		for i in range(len(data)):
			if self.Validate(41):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def Cooperative(self):
		data = self.DataPages(self.list_pages[42]).dropna()
		for i in range(len(data)):
			if self.Validate(42):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0

	def TaxLiens(self):
		data = self.DataPages(self.list_pages[43]).dropna()
		for i in range(len(data)):
			if self.Validate(43):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def SupplementaryPlan(self):
		data = self.DataPages(self.list_pages[44]).dropna()
		for i in range(len(data)):
			if self.Validate(44):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def Education(self):
		data = self.DataPages(self.list_pages[45]).dropna()
		for i in range(len(data)):
			if self.Validate(45):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0

	def Fefund(self):
		data = self.DataPages(self.list_pages[46]).dropna()
		for i in range(len(data)):
			if self.Validate(46):
				self.TotalsDeductions += float(data['Valor'].values[i])
				return "{:.2f}".format(data['Valor'].values[i])
		return 0


	def Debt(self):
		data = self.DataPages(self.list_pages[47]).dropna()
		for i in range(len(data)):
			if self.Validate(47):
				return "{:.2f}".format(data['Valor'].values[i])
		return 0

	def DeductionsTotal(self):
		return self.TotalsDeductions

	def WorkedDays(self):
		data = self.DataPages(self.list_pages[0]).dropna()
		for i in range(len(data)):
			if self.Validate(0):
				return "{:.2f}".format(data['Dias Trabajdos'].values[i])
		return 0

	def Transport(self):
		data = self.DataPages(self.list_pages[0]).dropna()
		for i in range(len(data)):
			if self.Validate(0):
				return "{:.2f}".format(data['Dias Trabajdos'].values[i])
		return 0


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

class SendPayroll:


	def __init__(self,documentI,path):
		self.dni = documentI
		self.pc = PayRollCustom(path,documentI)

	def Period(self):
		return {
					"admision_date": "2021-12-10",
			        "settlement_start_date": "2021-12-10",
			        "settlement_end_date": "2021-12-15",
			        "worked_time": "15.00",
			        "issue_date": "2021-12-10"
			    }

	def Accrued(self):
		return {
			"worked_days": self.pc.WorkedDays(),
	        "salary": "750000.00",
	        "transportation_allowance":"109000.00",
	        "HEDs": self.pc.ExtraHour(),
	        "HENs": self.pc.ExtraNightTime(),
	        "HRNs": self.pc.ExtraHourNightSurcharge(),
	        "HEDDFs": self.pc.SundayExtraDaytime(),
	        "HRDDFs": self.pc.ExtraHourDaytimeSurcharge(),
	        "HENDFs": self.pc.SundayExtraNightTime(),
	        "HRNDFs": self.pc.ExtraHourNightSurchargeSun(),
	        "common_vacation" : self.pc.Vacations(),
	        "paid_vacation":self.pc.CompensatedVacationDays(),
	        "service_bonus": self.pc.ServiceBonus(),
	        "severance":self.pc.ServiceBonus(),
	        "work_disabilities":self.pc.WorkDisabilities(),
	        "maternity_leave":self.pc.MaternityLeave(),
	        "paid_leave":self.pc.PaidLeave(),
	        "non_paid_leave":self.pc.PaidNotLeave(),
	        "bonuses":self.pc.BonusSocial(),
	        "aid":self.pc.SalaryAssistant(),
	        "legal_strike": self.pc.LegalStrike(),
	        "other_concepts":self.pc.OtherConcepts(),
	        "compensations":self.pc.Compensations(),
	        "epctv_bonuses":self.pc.EpctvBonuses(),
	        "commissions":self.pc.Commissions(),
	        "third_party_payments":self.pc.ThirdPartyPayments(),
	        "advances":self.pc.Advances(),
	        
	        "sustenance_support":self.pc.SustenanceSupport(),
	        "withdrawal_bonus":self.pc.Telecommuting(),
	        "compensation":self.pc.Compensation(),
	        "accrued_total":"100000",
		}

	def Deductions(self):
		return {
			"eps_type_law_deductions_id": 1,
	        "eps_deduction": self.pc.EPSDeduction(),
	        "pension_type_law_deductions_id": 5,
	        "pension_deduction": self.pc.PensionDeduction(),
	        "labor_union":self.pc.LaborUnion(),
	        "sanctions":self.pc.Sanctions(),
	        "orders":self.pc.Orders(),
	        "third_party_payments":self.pc.ThirdPartyPayments(),
	        "advances":self.pc.Advances(),
	        "other_deductions":self.pc.OtherDeductions(),
	        "voluntary_pension":self.pc.VoluntaryPension(),
	        "withholding_at_source":self.pc.WithholdingAtSource(),
	        "afc":self.pc.AFC(),
	        "cooperative":self.pc.Cooperative(),
	        "tax_liens":self.pc.TaxLiens(),
	        "supplementary_plan":self.pc.SupplementaryPlan(),
	        "education":self.pc.Education(),
	        "refund":self.pc.Fefund(),
	        "debt":self.pc.Debt(),
	        "deductions_total": "120000.00"
		}

	def Period(self):
		return {
			"admision_date": "2021-12-10",
			"settlement_start_date": "2021-12-10",
			"settlement_end_date": "2021-12-15",
			"worked_time": "15.00",
			"issue_date": "2021-12-10"
		}
