from passlib.hash import sha512_crypt
from connectwrap import db
from pydate import DateTime
from flask import render_template, url_for, request, redirect, flash, abort
from app import app
from app.forms import LoginForm, RegisterForm
from app.user import User

user_db = db("app/users.db", "Users"); user_db.close_db()
user = User()

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home'), 200

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='Sign In', form=LoginForm()), 200

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html', title='Register', form=RegisterForm()), 200

@app.route('/register_user', methods=['POST'])
def register_user():
    if (request.method == 'POST'):
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        account_type = "Standard"
        user_db.open_db()

        if (user_db.get_row("Email", email) == None and user_db.get_row("Username", username) == None):
            last_updated = DateTime()
            last_updated.set_UTC()
            user_db.insert_row(email, username, sha512_crypt.hash(password + last_updated.tostring()), account_type, last_updated.tostring())
            user_db.close_db()
            flash(str("Account Created! Welcome {0}!").format(username))
            user.is_authenticated = True
            return render_template("account.html", title='Account', email=email, username=username, type=account_type), 201
        else:
            user_db.close_db()
            flash("Account registration failed! An account with that Email and/or Username already exists!")
            return redirect(url_for('register')), 301
    else:
        abort(405)

@app.route('/login_user', methods=['POST'])
def login_user():
    if (request.method == 'POST'): 
        username = request.form['username']
        password = request.form['password']
        user_db.open_db()
        row = user_db.get_row("Username", username)

        try:
            if (row["Username"] == username and sha512_crypt.verify(password + row["LastUpdated"], row["Password"]) == True and row["Type"] != "Admin"):
                user_db.close_db()
                flash(str("Welcome User {0}!").format(username))
                user.is_authenticated = True
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"]), 200
            elif (row["Username"] == username and sha512_crypt.verify(password + row["LastUpdated"], row["Password"]) == True and row["Type"] == "Admin"):
                users = user_db.get_table()
                user_db.close_db()
                flash(str("Welcome Admin {0}!").format(username))
                user.is_authenticated = True
                return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users), 200
            else:
                user_db.close_db()
                flash("Login failed! Either the Username or Password was incorrect!")
                return redirect(url_for('login')), 301
        except:
            user_db.close_db()
            flash("Login failed! Either the Username or Password was incorrect!")
            return redirect(url_for('login')), 301
    else:
        abort(405)
            
@app.route('/del_user', methods=['POST'])
def del_user(): 
    if (request.method == 'POST'):
        if (user.is_authenticated == False):
            abort(401)

        username = request.form['username']
        user_db.open_db()
        row = user_db.get_row("Username", username)

        if (row["Type"] == "Admin"):
            users = user_db.get_table()
            user_db.close_db()
            flash("Error! Can't delete an Admin account!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users), 406
        else:
            user_db.drop_row("Username", username)
            user_db.close_db()
            flash(str("User {0} successfully deleted!").format(username))
            return render_template("index.html", title='Home'), 200
    else:
        abort(405)

@app.route('/change_password', methods = ['POST'])
def change_password():
    if (request.method == 'POST'):
        if (user.is_authenticated == False):
            abort(401)
        
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        last_updated = DateTime()
        last_updated.set_UTC()
        user_db.open_db()
        row = user_db.get_row("Username", username)

        try:
            if (row != None and row["Username"] == username and sha512_crypt.verify(password + row["LastUpdated"], row["Password"]) == True and row["Type"] != "Admin"):
                user_db.update_row("Password", sha512_crypt.hash(new_password + last_updated.tostring()), "Username", username)
                user_db.update_row("LastUpdated", last_updated.tostring(), "Username", username)
                user_db.close_db()
                flash("Password changed successfully!")
                return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"]), 200
            elif (row != None and row["Username"] == username and sha512_crypt.verify(password + row["LastUpdated"], row["Password"]) == True and row["Type"] == "Admin"):
                user_db.update_row("Password", sha512_crypt.hash(new_password + last_updated.tostring()), "Username", username)
                user_db.update_row("LastUpdated", last_updated.tostring(), "Username", username)
                users = user_db.get_table()
                user_db.close_db()
                flash("Password changed successfully!")
                return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users), 200
            else:
                user_db.close_db()
                flash("Password change failed! The current password provided is incorrect! Please login with the correct password!")
                return redirect(url_for('login')), 301
        except:
            user_db.close_db()
            flash("Password change failed! The current password provided is incorrect! Please login with the correct password!")
            return redirect(url_for('login')), 301
    else:
        abort(405)

@app.route('/change_username', methods = ['POST'])
def change_username():
    if (request.method == 'POST'):
        if (user.is_authenticated == False):
            abort(401)

        username = request.form['username']
        new_username = request.form['new_username']
        user_db.open_db()

        if (user_db.get_row("Username", new_username) == None and user_db.get_row("Username", username)["Type"] != "Admin"):
            user_db.update_row("Username", new_username, "Username", username)
            row = user_db.get_row("Username", new_username)
            user_db.close_db()
            flash("Username changed successfully!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"]), 200
        elif (user_db.get_row("Username", new_username) == None and user_db.get_row("Username", username)["Type"] == "Admin"):
            user_db.update_row("Username", new_username, "Username", username)
            row = user_db.get_row("Username", new_username)
            users = user_db.get_table()
            user_db.close_db()
            flash("Username changed successfully!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users), 200
        elif (user_db.get_row("Username", new_username) != None and user_db.get_row("Username", username)["Type"] == "Admin"):
            row = user_db.get_row("Username", username)
            users = user_db.get_table()
            user_db.close_db()
            flash("Username change failed! That username already exists!")
            return render_template("admin.html", title='Admin Account', email=row["Email"], username=row["Username"], type=row["Type"], users=users), 400
        else:
            row = user_db.get_row("Username", username)
            user_db.close_db()
            flash("Username change failed! That username already exists!")
            return render_template("account.html", title='Account', email=row["Email"], username=row["Username"], type=row["Type"]), 400
    else:
        abort(405)