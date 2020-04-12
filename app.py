from flask import Flask
from flask import render_template, request
import os
import PyPDF2
import types
import re
import fitz
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("Home.html")

def pdf_scrapper(filenames):
    dictForm = {}
    doc = fitz.open(filenames)  
    pages = doc.pageCount
    text = ""
    link = []
    dictForm['name']=''
    dictForm['email'] = ''
    dictForm['phone'] = ''
    dictForm['linkedin'] = ''
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
    dictForm['textCount'] = len(text2.strip())
    #End

    #Finding name, email, and linkedin profile
    contentList = text.split("\n")

    if(contentList[0].rstrip().lstrip() == "RESUME"):
        dictForm['name'] = contentList[2].lstrip().rstrip()

    for i in link:
        if "linkedin" in i:
            dictForm['linkedin'] = i.lstrip().rstrip()
        if "@" in i:
            dictForm['email'] = i[str(i).find(":"):].lstrip().rstrip().split(':')[1]
    #End find name,etc

    #finding contact number
    print(dictForm)
    return dictForm

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        path = os.path.join(os.getcwd())
        f.save(path+f.filename)
        details = pdf_scrapper(f.filename)
        os.remove(path+f.filename)
        name = details["name"]
        email = details["email"]
        phone = details["phone"]
        linkedin = details["linkedin"]
        linecount = details["lineCount"]
        textcount = details["textCount"]
        tablecount = details["tableCount"]
        imgcount = details["imgCount"]
        print(linkedin)
        conn = sqlite3.connect(os.path.join(path,'database.db'))
        c = conn.cursor()
        c.execute('SELECT * FROM userdetails WHERE Email=?', [email])
        res = c.fetchone()
        conn.commit()
        conn.close()
        if(res == None):
            return render_template("resume.html",name=name,
                                             email=email,
                                             phone=phone,
                                             linkedin=linkedin,
                                             linecount=linecount,
                                             textcount=textcount,
                                             tablecount=tablecount,
                                             imgcount=imgcount)
        else:
            return "Email Already Exits"
    else:
        return "error"

@app.route('/datasave', methods=['GET', 'POST'])
def form_handle():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        linkedin = request.form["linkedin"]
        linecount = request.form["linecount"]
        textcount = request.form["textcount"]
        tablecount = request.form["tablecount"]
        imgcount = request.form["imgcount"]
        fontstyle = request.form["fontstyle"]
        fontsize = request.form["fontsize"]
        conn = sqlite3.connect('C:/Users/Aniruddha/Documents/Resume-master/database.db')
        c = conn.cursor()
        c.execute("INSERT INTO userdetails VALUES (?,?,?,?,?,?,?,?,?,?)",(name,email,phone,linkedin,linecount,textcount,tablecount,imgcount,fontstyle,fontsize))
        # Save (commit) the changes
        conn.commit()
        conn.close()
        return "Uploaded Data Successfully"
    else:
        return "Error"
    return "Error"
if __name__ == '__main__':
    app.run(debug=True)