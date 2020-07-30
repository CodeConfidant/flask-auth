from connectwrap import db
from flask import render_template, url_for, request
from app import app

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register')

@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db = db("app/users.db")
        message = ""

        if (user_db.get_row("users", "Username", username) == None):
            user_db.insert_row("users", username, password)
            message = "Account Created!"
        else:
            message = "Account Creation Failed!"
        
        user_db.close_db()
        return render_template("result.html", title='Result', message=message)

@app.route('/loginuser', methods = ['POST', 'GET'])
def loginuser():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db = db("app/users.db")
        message = ""

        try:
            if (user_db.get_row("users", "Username", username)["Username"] == username and user_db.get_row("users", "Password", password)["Password"] == password):
                message = "Welcome " + username
        except:
            message = "User Login Failed! Either the username or password is incorrect!"
        finally:
            user_db.close_db()
            return render_template("result.html", title='Result', message=message)