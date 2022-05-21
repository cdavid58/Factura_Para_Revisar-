import requests,sqlite3,json
from api.translator import Translator

t = Translator()

# url = "http://localhost:8000/api/Create_Invoice_"
# for i in range(1,10000):
#   print(i)
#   payload = json.dumps({
#     "payment_form": {
#       "payment_form_id": 1,
#       "payment_method_id": 10,
#       "payment_due_date": "2022-03-22",
#       "duration_measure": "0"
#     },
#     "invoice_lines": {
#       "number": i,
#       "prefix": "FE",
#       "code": 50001,
#       "quanty": 1,
#       "description": "Teclado",
#       "price": 100,
#       "tax": 0,
#       "notes": "Proof of electronic billing",
#       "date": "2022-03-22",
#       "ipo": 0,
#       "discount": 0,
#       "client": 900166483,
#       "company": 12345678990,
#       "empleoyee":987654321
#     }
#   })
#   headers = {
#     'Content-Type': 'application/json'
#   }
#   response = requests.request("POST", url, headers=headers, data=payload)
#   print(response.text)


con = sqlite3.connect('db.sqlite3')
c = con.cursor()
c.execute("delete from invoice_Payment_Form_Invoice")
# for i in range(1,100000):
#   query = """insert into invoice_Invoice(
#             number,prefix,code,quanty,description,price,
#             tax,notes,date,ipo,discount,client_id,company_id,
#             type,state,empleoyee_id
#           ) 
#           values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
#   args = (
#       t.codificar(str(i)),
#       '1000110,1000101',
#       '110101,110000,110000,110000,110001',
#       '110001',
#       '1010100,1100101,1100011,1101100,1100001,1100100,1101111',
#       '110001,110000,110000',
#       '110000',
#       '1010000,1110010,1101111,1101111,1100110,100000,1101111,1100110,100000,1100101,1101100,1100101,1100011,1110100,1110010,1101111,1101110,1101001,1100011,100000,1100010,1101001,1101100,1101100,1101001,1101110,1100111',
#       '110010,110000,110010,110010,101101,110000,110011,101101,110010,110010',
#       '110000',
#       '110000',
#       9,
#       4,
#       'FE',
#       '1010011,1101001,1101110,100000,1100101,1101110,1110110,1101001,1100001,1110010,100000,1100001,100000,1101100,1100001,100000,1000100,1001001,1000001,1001110',
#       10
#   )
#   c.execute(query,args)
con.commit()
