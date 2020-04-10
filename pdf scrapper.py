import PyPDF2
import os

resume = open("Resume_1.pdf","rb")
pdfReader = PyPDF2.PdfFileReader(resume)

totalPages = pdfReader.numPages
resumeContent = ""
#for i in range(totalPages):
    #pageObj = pdfReader.getPage(i)
    #resumeContent += pageObj.extractText()
#print(resumeContent)
PDF = PyPDF2.PdfFileReader(resume)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
ank = '/A'

for page in range(pages):
    print("Current Page: {}".format(page))
    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()
    if key in pageObject.keys():
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[ank].keys():
                print(u[ank][uri])