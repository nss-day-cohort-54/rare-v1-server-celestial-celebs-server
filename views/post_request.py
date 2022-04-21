import sqlite3
import json
from models import Post, Category, User

#def a get function to fetch a posts details for a single post
def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['content'])

        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['created_on'], data['active'])

        category = Category(data['category_id'], data['label'])

        post.user = user.__dict__
        post.category = category.__dict__


    return json.dumps(post.__dict__)


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        """)

        data = db_cursor.fetchall()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['content'])

        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['created_on'], data['active'])

        category = Category(data['category_id'], data['label'])

        post.user = user.__dict__
        post.category = category.__dict__


    return json.dumps(post.__dict__)