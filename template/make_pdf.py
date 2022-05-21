import pdfkit
def GeneratePDF(name_doc):
	pdfkit.from_file('template/pdfs/'+name_doc+'.html', name_doc+'.pdf')