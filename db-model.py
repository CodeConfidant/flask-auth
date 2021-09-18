import os
from passlib.hash import sha512_crypt
from connectwrap import db, utils
from pydate import DateTime

admin_email = str("master@test.com")
admin_username = str("master123")
last_updated = DateTime(1111, 1, 1, 1, 1, 1)
last_updated.set_UTC()
admin_password = sha512_crypt.hash("master123" + last_updated.tostring())
account_type = "Admin"

if (os.path.exists("app/users.db") == False):
    utils.create_database("app/users.db")
    user_db = db("app/users.db", "Users")
    user_db.create_table("Users", Email = "str", Username = "str", Password = "str", Type = "str", LastUpdated = "str")
    user_db.insert_row(admin_email, admin_username, admin_password, account_type, last_updated.tostring())
    user_db.close_db()

elif (os.path.exists("app/users.db") == True):
    user_db = db("app/users.db", "Users")
    user_db.select_table()
    user_db.close_db()