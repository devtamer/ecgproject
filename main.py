from flask import Flask, render_template, url_for, request, redirect
import sqlite3 as sql

app = Flask(__name__)

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
                "Password" : request.form['pass']
            }   
            with sql.connect("HeartHealth.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (FirstName, LastName, Email, Password) VALUES(?,?,?,?)", (user["FirstName"], user["LastName"], user["Email"], user["Password"]))
                con.commit()
                con.close()
        except sql.Error as error:
            return render_template('404.html', error="SQL Error")
        finally:
            return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login")
    elif request.method == 'POST':
        try:
            with sql.connect("HeartHealth.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM user")
                results = cur.fetchall()
                for row in results:
                    email = row[3]
                    password = row[4]
                    if ((request.form['email'] == email) and (request.form['pass'] == password)):
                        return redirect(url_for('account', id=row[0]))
        except sql.Error:
            return render_template('404.html', error="SQL Error")

@app.route("/account/<id>")
def account(id):
    try:
        with sql.connect("HeartHealth.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM user WHERE Id = {id}")
            result = cur.fetchone()
            user = {
                "FirstName" : result[1],
                "LastName" : result[2],
                "Email" : result[3]
            }  
            return render_template('account.html', user=user)
    except sql.Error as error:
        return render_template('404.html', error="SQL Error")
        
if __name__ == '__main__':
    app.run()