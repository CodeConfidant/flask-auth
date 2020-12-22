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
            if (row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True and row["Type"] != "Admin"):
                user_db.close_db()
                flash(str("Welcome User {0}!").format(username))
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
            elif (row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True and row["Type"] == "Admin"):
                users = user_db.get_table()
                user_db.close_db()
                flash(str("Welcome Admin {0}!").format(username))
                return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)
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
            users = user_db.get_table()
            user_db.close_db()
            flash("Error! Can't delete an Admin account!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)
        else:
            user_db.drop_row("Username", username)
            users = user_db.get_table()
            user_db.close_db()
            flash(str("User {0} successfully deleted!").format(username))
            return render_template("index.html", title='Home')
    else:
        username = request.args.get('id')
        user_db.open_db()
        row = user_db.get_row("Username", username)

        if (row["Type"] == "Admin"):
            users = user_db.get_table()
            user_db.close_db()
            flash("Error! Can't delete an Admin account!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)
        else:
            user_db.drop_row("Username", username)
            users = user_db.get_table()
            user_db.close_db()
            flash(str("User {0} successfully deleted!").format(username))
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)

@app.route('/change_password', methods = ['POST', 'GET'])
def change_password():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        user_db.open_db()
        users = user_db.get_table()
        row = user_db.get_row("Username", username)

        try:
            if (row != None and row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True and row["Type"] != "Admin"):
                user_db.update_row("Password", sha512_crypt.hash(new_password), "Username", username)
                user_db.close_db()
                flash("Password changed successfully!")
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
            elif (row != None and row["Username"] == username and sha512_crypt.verify(password, row["Password"]) == True and row["Type"] == "Admin"):
                user_db.update_row("Password", sha512_crypt.hash(new_password), "Username", username)
                user_db.close_db()
                flash("Password changed successfully!")
                return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)
            else:
                user_db.close_db()
                flash("Password change failed! The current password provided is incorrect!")
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
        except:
            user_db.close_db()
            flash("Password change failed! The current password provided is incorrect!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])

@app.route('/change_username', methods = ['POST', 'GET'])
def change_username():
    if (request.method == 'POST'):
        username = request.form['username']
        new_username = request.form['new_username']
        user_db.open_db()

        if (user_db.get_row("Username", new_username) == None and user_db.get_row("Username", username)["Type"] != "Admin"):
            user_db.update_row("Username", new_username, "Username", username)
            row = user_db.get_row("Username", new_username)
            user_db.close_db()
            flash("Username changed successfully!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])
        elif (user_db.get_row("Username", new_username) == None and user_db.get_row("Username", username)["Type"] == "Admin"):
            user_db.update_row("Username", new_username, "Username", username)
            row = user_db.get_row("Username", new_username)
            users = user_db.get_table()
            user_db.close_db()
            flash("Username changed successfully!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users)
        else:
            row = user_db.get_row("Username", username)
            user_db.close_db()
            flash("Username change failed! That username already exists!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"])