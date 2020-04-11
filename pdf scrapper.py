import PyPDF2
import types
import os
import fitz

dictForm = {}
doc = fitz.open("Resume_1.pdf")  
pages = doc.pageCount

text = ""
link = []
for page in range(pages):
    for links in doc[page].getLinks():
        link.append(links['uri'])
    text += doc[page].getText("text")

contentList = text.split("\n")
#print(contentList)
if(contentList[0].rstrip().lstrip() == "RESUME"):
    dictForm['name'] = contentList[2].lstrip().rstrip()

for i in link:
    if "linkedin" in i:
        dictForm['linkedin'] = i.lstrip().rstrip()
    if "@" in i:
        dictForm['email'] = i[str(i).find(":"):].lstrip().rstrip()
print(dictForm)
