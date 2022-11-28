from flask import *
import sqlite3
from form import RegistrationForm
from form import Registration
import os
from werkzeug.utils import secure_filename
from random import *
from markupsafe import escape
from flask import *  
from flask_mail import Mail
from flask_mail import Message

from functools import wraps
from flask_wtf.csrf import CSRFError
from flask_wtf.csrf import CSRFProtect
app=Flask(__name__,template_folder='template')
app.secret_key="__privatekey__"
UPLOAD_FOLDER="static/pdf"
ALLOWED_EXTENTIONS={'txt','pdf','png','jpg','jpeg'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
csrf = CSRFProtect()
mail = Mail(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465     
app.config["MAIL_USERNAME"] = 'dineshkumarp2711@gmail.com'  
app.config['MAIL_PASSWORD'] = 'secpnhpufhizvuwj'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

import ibm_db
con=ibm_db.connect("DATABASE= bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bbz06446;PWD=XFhGFz42ebWBQ1n4",'','')
print(con)
print("connection successfull....")





conn=sqlite3.connect('jobupdate2.db')
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS up(name text,location text,salary text,description text,skill text)")
conn.commit()



def create_app():
    app = Flask(__name__)
    csrf.init_app(app)

#login_Required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'name' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

    

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/resumeenter/")
@login_required
def resume():
    return render_template("resumecre.html")

@app.route("/login",methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        userName=request.form['name']
        passWord=request.form['password']
       # con=ibm_db.connect("DATABASE= bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bbz06446;PWD=XFhGFz42ebWBQ1n4",'','')
        
        statement=f"SELECT*from user WHERE name='{userName}' AND password='{passWord}';"
        stmt=ibm_db.prepare(con,statement)            
        ibm_db.execute(stmt)
        res=ibm_db.fetch_assoc(stmt)
        print(res)
        if  res==False:
            error = 'Incorrect Username/Password.'
            return render_template("login.html", error=error)
        else:
            session['logged_in']=True
            session['name']=userName
            print("***********************************************************")
            return redirect(url_for('profile'))
            
        flash(error)    
    else:
        request.method=='GET'
        return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    s = session['name'];  
    return render_template("profile.html",name=s)

@app.route("/resumecreate")
@login_required
def resumeenter():
    return render_template("resumecre.html")
@app.route("/alljob")
def alljob(): 
    conn=sqlite3.connect('jobupdate2.db')
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("SELECT*from up")
    da=cur.fetchall()
    conn.close()     
    print(da)   
    return render_template("all.html",ult=da)
    
    
def method_name():
    pass
@app.route("/course")
@login_required
def course():
    return render_template("course.html")

@app.route("/update",methods=['GET','POST'])
@login_required
def update():
    updo=Registration()
    
    if request.method=='POST':
        try:
            name=request.form['name']
            skill=request.form['skill']
            location=request.form['location']
            description=request.form['description']
            salary=request.form['salary']
            conn=sqlite3.connect('jobupdate2.db')
            cur=conn.cursor()
            cur.execute("INSERT INTO up(name,skill,location,description,salary) values(?,?,?,?,?)",(name,skill,location,description,salary))
            conn.commit()
        except:
            flash("Error insert opration","danger")
        finally:
            return redirect(url_for("alljob"))
            conn.close()
    return render_template("update.html",form=updo)

    
@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        
        email=request.form['email']
        msg = mail.send_message(
        'Send Mail tutorial!',
        sender=[email],
        recipients=['dineshkumarp2711@gmail.com'],
        body="Congratulations you've succeeded!"
        )
        return "send message"
    return render_template("contact.html")

@app.route("/about")
@login_required
def about():
    return render_template("dasabout.html")

@app.route("/inter1")
@login_required
def inter1():
    return render_template("inter1.html")

@app.route("/inter2")
@login_required
def inter2():
    return render_template("inter2.html")

@app.route("/inter3")
@login_required
def inter3():
    return render_template("inter3.html")


@app.route("/care1")
@login_required
def care1():
    return render_template("care1.html")

@app.route("/care2")
@login_required
def care2():
    return render_template("care2.html")
@app.route("/care3")
@login_required
def care3():
    return render_template("care3.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS
@app.route("/register",methods=['GET','POST'])#,method=['GET','POST']
def register():
    registration=RegistrationForm()
    #con=ibm_db.connect("DATABASE= bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bbz06446;PWD=XFhGFz42ebWBQ1n4",'','')
    if request.method=='POST':
        if(request.form["name"]!="" and request.form["password"]!=""):
            pdf=request.files['pdf']
            name=request.form["name"]
            password=request.form["password"]
            email=request.form["email"]
            fullname=request.form["fullname"]
            age=request.form["age"]
            experience=request.form["experience"]
            number=request.form["number"]
            gender=request.form["gender"]
            jobrole=request.form["jobrole"]
            location=request.form["location"]
            skill=request.form["skill"]
            statement="SELECT*from user WHERE name=?"
            print("hello flask")
            print(con)            
            stmt=ibm_db.prepare(con,statement)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.execute(stmt)
            data=ibm_db.fetch_assoc(stmt)
            if data:
                return render_template("error.html")
           
            else:
                if not data and pdf and allowed_file(pdf.filename) :
                    filename=secure_filename(pdf.filename)
                    pdf.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    insert_sql="INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                    prep_stmt=ibm_db.prepare(con,insert_sql)
                    print(pdf.filename)
                    print(name)
                    print(email)
                    print(password)
                    print(skill)
                    print(location)
                    print(jobrole)
                    print(gender)
                    print(experience)
                    print(fullname)
                    print(age)
                    print(number)
                    ibm_db.bind_param(prep_stmt,1,pdf.filename)
                    ibm_db.bind_param(prep_stmt,2,name)
                    ibm_db.bind_param(prep_stmt,3,email)
                    ibm_db.bind_param(prep_stmt,4,password)
                    ibm_db.bind_param(prep_stmt,5,skill)
                    ibm_db.bind_param(prep_stmt,6,location)
                    ibm_db.bind_param(prep_stmt,7,jobrole)
                    ibm_db.bind_param(prep_stmt,8,gender)
                    ibm_db.bind_param(prep_stmt,9,experience)
                    ibm_db.bind_param(prep_stmt,10,fullname)
                    ibm_db.bind_param(prep_stmt,11,age)
                    ibm_db.bind_param(prep_stmt,12,number)
                    print(prep_stmt)
                    ibm_db.execute(prep_stmt)
                    
                    
                return render_template("login.html",succ="Registration Successfull!")
      
                   
    elif request.method =='GET':
        return render_template('signup.html',form=registration)

@app.route("/success")
def success():
    name=session.get('name',None)
    return render_template('success.html',gfgf=name)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("you have been logged out!")
    return redirect(url_for('login'))

@app.route("/career")
@login_required
def career():
    return render_template("career.html")

if __name__=='__main__':
    app.run(debug=True)