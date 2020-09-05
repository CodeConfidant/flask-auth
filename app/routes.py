from passlib.hash import sha512_crypt
from connectwrap import db
from flask import render_template, url_for, request
from app import app

user_db = db("app/users.db", "Users"); user_db.close_db()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

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
        user_db.open_db()

        if (user_db.get_row("Email", email) == None and user_db.get_row("Username", username) == None):
            user_db.insert_row(email, username, sha512_crypt.hash(password))
            user_db.close_db()
            return render_template("account.html", title='Account', message=str("Account Created! Welcome {0}!").format(username), email=email, username=username)
        else:
            user_db.close_db()
            return render_template('register.html', title='Register', message="Account Creation Failed! That username or email already exists!")

@app.route('/loginuser', methods = ['POST', 'GET'])
def loginuser():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db.open_db()
        row = user_db.get_row("Username", username)

        try:
            if (row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True):
                user_db.close_db()
                return render_template("account.html", title='Account', message=str("Welcome {0}!").format(username), email=row["Email"], username=row["Username"])
            else:
                user_db.close_db()
                return render_template("login.html", title='Login', message="User Login Failed! Either the username or password is incorrect!")
        except:
            user_db.close_db()
            return render_template("login.html", title='Login', message="User Login Failed! Either the username or password is incorrect!")

@app.route('/deluser')
def deluser(): 
        username = request.args.get('id')
        user_db.open_db()
        user_db.drop_row("Username", username)
        user_db.close_db()
        return render_template("index.html", title='Home', message=str("User {0} successfully deleted!").format(username))

@app.route('/changepassword', methods = ['POST', 'GET'])
def changepassword():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        user_db.open_db()
        row = user_db.get_row("Username", username)

        if (row != None and row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True):
            user_db.update_row("Password", sha512_crypt.hash(new_password), "Username", username)
            row = user_db.get_row("Username", username)
            user_db.close_db()
            return render_template("account.html", title='Account', message="Password changed successfully!", email=row["Email"], username=row["Username"])
        else:
            user_db.close_db()
            return render_template("login.html", title='Login', message="Password change failed! Either the username or password was incorrect!")