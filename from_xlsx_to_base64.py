from base64 import b64decode
import base64

def Create_Document64(path):
    with open(path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read())
        
def GetDocumentPayroll(base_64,payroll_name):
    bytes = b64decode(base_64, validate=True)
    f = open(payroll_name+'.xlsx', 'wb')
    f.write(bytes)
    f.close()