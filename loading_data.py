import sqlite3, pymysql.cursors,sqlite3
MyDB = pymysql.connect(host="159.203.170.123",port=3306,user="root",passwd="medellin100",db="payroll",charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor = MyDB.cursor()


data_mysql = [
	'type_document_identifications','type_organizations',
	'type_regimes','municipalities','type_documents','payment_forms',
	'payment_methods','type_workers','payroll_type_document_identifications',
	'type_contracts'
]
data_sqlite = [
	'Type_Document_Identification','Type_Organization','Type_Regime',
	'Municipality','Type_Document','Payment_Form','Payment_Method',
	'Type_Worker','Payroll_Type_Document_Identification','Type_Contract'
]

n = 0
con = sqlite3.connect('db.sqlite3')
c = con.cursor()
for i in data_mysql:
	cursor.execute("select * from "+i)
	data = cursor.fetchall()
	db = data_sqlite[n]
	for j in data:
		print(j['id'])
		query = "insert into data_"+db+"(_id,name)values(?,?)"
		args = (int(j['id']), str(j['name']))
		c.execute(query,args)
	print('\n')
	n += 1
con.commit()