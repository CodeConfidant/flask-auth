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

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html', title='Account')

@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
    if (request.method == 'POST'): 
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user_db = db("app/users.db")
        message = ""

        if (user_db.get_row("users", "Email", email) == None and user_db.get_row("users", "Username", username) == None):
            user_db.insert_row("users", email, username, password)
            message = "Account Created! Welcome " + username
            user_db.close_db()
            return render_template("account.html", title='Account', message=message, email=email, username=username, password=password)
        else:
            message = "Account Creation Failed! That username or email already exists!"
            user_db.close_db()
            return render_template('register.html', title='Register', message=message)

@app.route('/loginuser', methods = ['POST', 'GET'])
def loginuser():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db = db("app/users.db")
        message = ""
        row = user_db.get_row("users", "Username", username)

        try:
            if (row["Username"] == username and row["Password"] == password):
                message = "Welcome " + username
                user_db.close_db()
                return render_template("account.html", title='Account', message=message, email=row["Email"], username=username, password=password)
            else:
                message = "User Login Failed! Either the username or password is incorrect!"
                user_db.close_db()
                return render_template("login.html", title='Login', message=message)
        except:
            message = "User Login Failed! Either the username or password is incorrect!"
            user_db.close_db()
            return render_template("login.html", title='Login', message=message)