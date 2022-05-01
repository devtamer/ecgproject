from flask import Flask, render_template, url_for, request
from database_handler import Database_Handler

db = Database_Handler()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title="Register")
    else:
        user = {
            "FirstName" : request.form['fname'],
            "LastName" : request.form['lname'],
            "Email" : request.form['email'],
            "Password" : request.form['pass']
        }
        db.insert_user(user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login")
    else:
        pass
    
if __name__ == '__main__':
    app.run()