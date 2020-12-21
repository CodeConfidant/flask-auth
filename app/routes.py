from passlib.hash import sha512_crypt
from connectwrap import db
from flask import render_template, url_for, request, redirect, flash
from app import app
from app.forms import LoginForm, RegisterForm

user_db = db("app/users.db", "Users"); user_db.close_db()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Sign In', form=LoginForm())

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register', form=RegisterForm())

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html', title='Account')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if (request.method == 'POST'):
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user_db.open_db()

        try:
            if (user_db.get_row("Email", email) == None and user_db.get_row("Username", username) == None):
                user_db.insert_row(email, username, sha512_crypt.hash(password), "Standard")
                user_db.close_db()
                flash(str("Account Created! Welcome {0}!").format(username))
                return render_template("account.html", title='Account', email=email, username=username, type="Standard")
            else:
                user_db.close_db()
                flash("Account registration failed! An account with that Email and/or Username already exists!")
                return redirect(url_for('register'))
        except:
            user_db.close_db()
            flash("Account registration failed! An account with that Email and/or Username already exists!")
            return redirect(url_for('register'))

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db.open_db()
        row = user_db.get_row("Username", username)

        try:
            if (row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True):
                user_db.close_db()
                flash(str("Welcome {0}!").format(username))
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
            else:
                user_db.close_db()
                flash("Login failed! Either the Username or Password was incorrect!")
                return redirect(url_for('login'))
        except:
            user_db.close_db()
            flash("Login failed! Either the Username or Password was incorrect!")
            return redirect(url_for('login'))
            

@app.route('/del_user', methods=['GET', 'POST'])
def del_user(): 
    if (request.method == 'POST'):
        username = request.form['username']
        user_db.open_db()
        row = user_db.get_row("Username", username)
        if (row["Type"] == "Admin"):
            user_db.close_db()
            flash("Error! Can't delete an Admin account!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
        else:
            user_db.drop_row("Username", username)
            user_db.close_db()
            flash(str("User {0} successfully deleted!").format(username))
            return render_template("index.html", title='Home')