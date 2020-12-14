import os
from passlib.hash import sha512_crypt
from connectwrap import db, utils

admin_email = str("master@test.com")
admin_username = str("master123")
admin_password = sha512_crypt.hash("master123")

if (os.path.exists("app/users.db") == False):
    utils.create_database("app/users.db")
    user_db = db("app/users.db", "Users")
    user_db.create_table("Users", Email="str", Username="str", Password="str", Type="str")
    user_db.insert_row(admin_email, admin_username, admin_password, "Admin")
    user_db.close_db()

elif (os.path.exists("app/users.db") == True):
    user_db = db("app/users.db", "Users")
    user_db.select_table()
    user_db.close_db()