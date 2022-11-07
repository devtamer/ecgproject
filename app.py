from flask import Flask, render_template,flash, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user 
from flask_bcrypt import Bcrypt
from forms import LoginForm
import sqlite3
import os

# for send_email function to be implemented
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib, ssl

app = Flask(__name__)
SKEY = os.urandom(32)
app.config['SECRET_KEY'] = SKEY
bcrypt = Bcrypt(app)
# handles login/authentication 
login_manager = LoginManager(app)
login_manager.login_view = "login"
# sql db 
heartdb = 'heart.db'

class User(UserMixin):
    def __init__(self, id, firstName, lastName, phoneNumber, email, password):
         self.id = str(id)
         self.firstname = firstName
         self.lastname = lastName
         self.phonenumber = phoneNumber
         self.email = email
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title="Register")
    elif request.method == 'POST':
        try:
            user = {
                "FirstName" : request.form['fname'],
                "LastName" : request.form['lname'],
                "Email" : request.form['email'],
                "Password" : bcrypt.generate_password_hash(request.form['pass'])
            }   
            with sqlite3.connect(heartdb) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (FirstName, LastName, Email, Password) VALUES(?,?,?,?)", (user["FirstName"], user["LastName"], user["Email"], user["Password"]))
                con.commit()
                con.close()
        except sqlite3.Error:
            return render_template('404.html', error="SQL Error")
        finally:
            return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
   conn = sqlite3.connect(heartdb)
   curs = conn.cursor()
   curs.execute("SELECT * from user where id = (?)",[id])
   lu = curs.fetchone()
   if lu is None:
    return None
   else:
    return User(int(lu[0]),lu[1],lu[2],lu[5], lu[3], lu[4])

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',title='Login', form=form)
    elif request.method == 'POST':
        try:
            con = sqlite3.connect(heartdb)
            cur = con.cursor()
            cur.execute("SELECT * FROM user where email = (?)",  [form.email.data])
            user = list(cur.fetchone())
            Us = load_user(user[0])
            if(form.email.data == Us.email and bcrypt.check_password_hash(Us.password, form.password.data)):
                login_user(Us, remember=form.remember.data)
                Umail = list({form.email.data})[0].split('@')[0]
                flash('Logged in successfully '+Umail)
                return redirect(url_for('results', id=Us.id))
            else:
                flash('Login Unsuccessfull.')
        except sqlite3.Error:
                return render_template('404.html', error="SQL Error")

def send_email(recipient, ecgbpm, ecgpng):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "ecgproject578@gmail.com"
    password = "578wireless$$"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "Your ECG Results"
    msg.attach(MIMEText(ecgbpm, 'plain'))
    body = "Link: http://127.0.0.1:5000"
    body = MIMEText(body)
    msg.attach(body)
    img_data = open(ecgpng, 'rb')
    image = MIMEImage(img_data.read(), name=os.path.basename(ecgpng))
    msg.attach(image)

    context = ssl.create_default_context()
    try:
        smtp_server = smtplib.SMTP(smtp_server, port)
        smtp_server.starttls(context=context)
        smtp_server.login(sender_email, password)
        smtp_server.sendmail( sender_email, recipient, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        smtp_server.quit()

@app.route("/results/<id>")
def results(id):
    try:
        con = sqlite3.connect(heartdb)
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE id = ?", [id])
        result = cur.fetchone()
        user = {
            "ID": result[0],
            "FirstName" : result[1],
            "LastName" : result[2],
            "Email" : result[3],
            "PhoneNumber": result[5]
        }  
        return render_template('results.html', user=user, id=id)

    except sqlite3.Error:
        return render_template('404.html', error="Error Verifying User")

@app.route("/profile/<id>")
def profile(id):
    if request.method == 'GET':
        print("entered get method from profile")
        cur = con.curser()
        cur.execute("SELECT * FROM user WHERE Id = ?", id )
        result = cur.fetchone()
        print(result)
        return render_template('profile.html', title="Profile")
    elif request.method == 'POST':
        try:
            newuser = {
                "FirstName" : request.form['fname'],
                "LastName" : request.form['lname'],
                "Email" : request.form['email'],
                "Phone Number": request.form['phonenumber']
            }
            with sqlite3.connect(heartdb) as con:
                cur = con.curser()
                cur.execute("SELECT * FROM user WHERE Id = ?", id )
                result = cur.fetchone()
                user = {
                    "FirstName" : result[1],
                    "LastName" : result[2],
                    "Email" : result[3]
                }  
                return render_template('profile.html', user=user, id=id)
        except sqlite3.Error:
            return render_template('404.html', error="Error Updating User")



if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.debug = True
    app.run()
