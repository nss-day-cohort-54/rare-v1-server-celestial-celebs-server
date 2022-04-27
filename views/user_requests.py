

import json
import sqlite3

from models.user import User

# function gets all users
def get_all_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        ORDER BY u.username ASC
        """)

        users = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['created_on'], row['active'], row['profile_image_url'])
            users.append(user.__dict__)
    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['created_on'], data['active'], data['profile_image_url'])
            


    return json.dumps(user.__dict__)