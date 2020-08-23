import os
from connectwrap import db, utils

if (os.path.exists("app/users.db") == False):
    utils.create_database("app/users.db")
    user_db = db("app/users.db")
    user_db.create_table("users", Email="str", Username="str", Password="str")
    user_db.insert_row("users", "master@test.com", "master123", "master123")
    user_db.close_db()

elif (os.path.exists("app/users.db") == True):
    user_db = db("app/users.db")
    user_db.select_table("users")
    user_db.close_db()