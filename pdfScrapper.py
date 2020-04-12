import fitz
def pdf_scrapper(filenames):
    dictForm = {}
    doc = fitz.open(filenames)  
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
    dictForm['fontname'] = None
    dictForm['fontsizes'] = None

    for page in range(pages):

        #Find Links like email and linkedin profile
        for links in doc[page].getLinks():
            link.append(links['uri'])
        text += doc[page].getText("text")
        #End find links

    #Still not able to find a feasible way to find number of tables in pdf

    #Find number of Images
    dictForm['imgCount'] = len(doc.getPageImageList(page))
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
    else:
        if text2.split()[0] == text2.split()[1]:
            dictForm['name'] = text2.split()[0].lstrip().rstrip()
        else:
            dictForm['name'] = text2.split()[0].lstrip().rstrip() + " " + text2.split()[1].lstrip().rstrip()

    for i in link:
        if "linkedin" in i:
            dictForm['linkedin'] = i.lstrip().rstrip()
        if "@" in i:
            dictForm['email'] = i[str(i).find(":"):].lstrip().rstrip().strip(":")
    #End find name,etc

    #finding contact number

    #find font-details

    #get fonts info
    fontDetails = {}
    for page in doc:
        for fonts in page.getFontList():
            fname = fonts[3][(fonts[3].find("+")+1):]
            fsize = fonts[0]
            if  fsize is not None and fname is not None:
                if (fname in fontDetails) and (str(fsize) not in fontDetails[fname]):
                    fontDetails[fname] +=  ("/" +str(fsize))  
                else:
                    fontDetails[fname] = str(fsize)

    dictForm['fontname'] = dictForm['fontsizes'] = ""
    for name,sizes in fontDetails.items():  
        dictForm['fontname'] += (name + ",") 
        dictForm['fontsizes'] += ("(" + sizes +"),")
    
    dictForm['fontname'] = dictForm['fontname'].rstrip(',').lstrip().rstrip()
    dictForm['fontsizes']= dictForm['fontsizes'].rstrip(',').lstrip().rstrip()

    return dictForm