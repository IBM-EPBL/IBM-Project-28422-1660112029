from flask_wtf import Form
from wtforms import TelField,PasswordField,EmailField,SubmitField,IntegerField,RadioField,FileField,SelectField,TextAreaField
from wtforms.validators import ValidationError,DataRequired

class RegistrationForm(Form):
    pdf=FileField(label="UploadResume",validators=[DataRequired()])
    fullname=TelField(label="Fullname",validators=[DataRequired()])
    name=TelField(label="Username",validators=[DataRequired()])
    email=EmailField(label="Email",validators=[DataRequired()])
    skill=TelField(label="Skills",validators=[DataRequired()])
    jobrole=SelectField(label="Jobrole",choices=[("select job"),("Java developer"),("python developer"),("software engineer"),("fontend"),("backend"),("senior java developer"),("junior java developer"),("HR"),("senior python developer")],validators=[DataRequired()])
    experience=SelectField(label="Experience",choices=[("student"),("Freshers"),("1year"),("2year"),("3year")],validators=[DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    number=IntegerField(label="Mobile number",validators=[DataRequired()])
    age=IntegerField(label="Age",validators=[DataRequired()])
    gender=RadioField(label="Gender",choices=["Male","Female"],validators=[DataRequired()])
    location=TelField(label="Location",validators=[DataRequired()])
    submit=SubmitField("Register")
    
class Registration(Form):
    skill=TelField(label="Skill",validators=[DataRequired()])
    name=TelField(label="Job Name",validators=[DataRequired()])
    salary=TelField(label="Salary",validators=[DataRequired()])
    description=TextAreaField(label="Description")
    location=TelField(label="Location",validators=[DataRequired()])
    submit=SubmitField("Update")
    
