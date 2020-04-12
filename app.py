from flask import Flask
from flask import render_template, request, send_file
import os
import sqlite3
import pdfScrapper as ps
import docxScrapper as ds


app = Flask(__name__)

#Routes

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/aboutus", methods=['GET', 'POST'])
def aboutus():
    return render_template("about.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    details = None
    f = None
    if request.method == 'POST':
        f = request.files['file']
        path = os.path.join(os.getcwd())
        f.save(path+f.filename)

        if f is None:
            return render_template("home.html")

        elif(str(f.filename).endswith(".pdf")):
            details = ps.pdf_scrapper(f.filename)
        else:
            details = ds.docxScrapper(f.filename)

        os.remove(path+f.filename)
        if details is not None:
            name = details["name"]
            email = details["email"]
            phone = details["phone"]
            linkedin = details["linkedin"]
            linecount = details["lineCount"]
            textcount = details["textCount"]
            tablecount = details["tableCount"]
            imgcount = details["imgCount"]
            fontnames = details["fontname"]
            fontsizes = details["fontsizes"]
            return render_template("resume.html",name=name,
                                                email=email,
                                                phone=phone,
                                                linkedin=linkedin,
                                                linecount=linecount,
                                                textcount=textcount,
                                                tablecount=tablecount,
                                                imgcount=imgcount,
                                                fontnames = fontnames,
                                                fontsizes = fontsizes
                                                )
        else:
            return "error"
    else:
        return "No details found!!!"

@app.route('/download')
def download():
    Resume_master = os.path.join(os.getcwd(),"Resume-master") 
    conn = sqlite3.connect(os.path.join(Resume_master,"database.db"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdetails")
    rows = cur.fetchall()
    lis = []
    for row in rows:
        print(list(row))
        lis.append(list(row))
    
    import csv  
        
    # field names  
    fields = ['Name', 'Email', 'Phone', 'Linked_In', 'text_line',
                'text_char','notable','noimage','fontstyle','fontsize']  
        
    # data rows of csv file  
        
    # name of csv file  
    filename = os.path.join(Resume_master,"download.csv")
        
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)  
        # writing the data rows  
        csvwriter.writerows(lis) 
    
    #return send_file(filename, as_attachment=True)
    return render_template("resume.html")
@app.route('/datasave', methods=['GET', 'POST'])
def form_handle():
    if request.method == 'POST':
        if request.form["name"] is None or request.form["name"] == "":
            name = "NULL"
        else:
            name = request.form["name"]
        
        if request.form["email"] is "None" or request.form["email"] == "":
            email = "NULL"
        else:
            email = request.form["email"]

        if request.form["phone"] is "None" or request.form["phone"] == "":
            phone = "NULL"
        else:
            phone = request.form["phone"]
        
        if request.form["linkedin"] is "None" or request.form["linkedin"] == "":
            linkedin = "NULL"
        else:
            linkedin = request.form["linkedin"]
        
        linecount = request.form["linecount"]
        textcount = request.form["textcount"]
        tablecount = request.form["tablecount"]
        imgcount = request.form["imgcount"]
        fontstyle = request.form["fontstyle"]
        fontsize = request.form["fontsize"]
        
        Resume_master = os.path.join(os.getcwd(),"Resume-master") 
        conn = sqlite3.connect(os.path.join(Resume_master,"database.db"))

        #Check if email exists
        c = conn.cursor()
        c.execute('SELECT * FROM userdetails WHERE Email=?', [email])
        res = c.fetchone()
        conn.commit()
        
        if(res == None):
            c = conn.cursor()
            c.execute("INSERT INTO userdetails VALUES (?,?,?,?,?,?,?,?,?,?)",(name,email,phone,linkedin,linecount,textcount,tablecount,imgcount,fontstyle,fontsize))
            conn.commit()
        else:
            return "Email Already Exists"
        conn.close()
        #done checking
        return "Uploaded Data Successfully"

    else:
        return "Error"

    return "Error"

if __name__ == '__main__':
    app.run(debug=True)