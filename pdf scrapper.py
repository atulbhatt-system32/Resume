import PyPDF2
import types
import os
import fitz
import re


dictForm = {}
doc = fitz.open("Resume_2.pdf")  
pages = doc.pageCount
text = ""
link = []
dictForm['name']=None
dictForm['email'] = None
dictForm['phone'] = None
dictForm['linkedin'] = None
dictForm['lineCount'] = 0
dictForm['textCount'] = 0
dictForm['tableCount'] = 0
dictForm['imgCount'] = 0

for page in range(pages):

    #Find Links like email and linkedin profile
    for links in doc[page].getLinks():
        link.append(links['uri'])
    text += doc[page].getText("text")
    #End find links

#Find number of Images
for img in doc.getPageImageList(page):
    dictForm['imgCount'] += 1
#End find images

#Find total number of Lines in the file
dictForm['lineCount'] = text.count("\n")
#End search for total Lines

#Removing new-lines '\n' form the file to count only the words
flag = True

text1 = text
text2 = ""
while(flag):
    text2 = text1.replace("\n"," ").replace("  "," ")
    if(text2 == text1):
        flag = False
    else:
        text1 = text2

#End cleaning the "text" with '\n'

#Finding the number of words"
dictForm['textCount'] = len(text2.strip(" "))
#End

#Finding name, email, and linkedin profile
contentList = text.split("\n")

if(contentList[0].rstrip().lstrip() == "RESUME"):
    dictForm['name'] = contentList[2].lstrip().rstrip()

for i in link:
    if "linkedin" in i:
        dictForm['linkedin'] = i.lstrip().rstrip()
    if "@" in i:
        dictForm['email'] = i[str(i).find(":"):].lstrip().rstrip()
#End find name,etc

#finding contact number

print(dictForm)