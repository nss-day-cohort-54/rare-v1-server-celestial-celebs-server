import json
import sqlite3
from models import User
from models.comment import Comment
from models.post import Post

def get_all_post_comments(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active,
            u.profile_image_url
        FROM Comments c
        JOIN Users u
            ON c.author_id = u.id
        WHERE c.post_id = ?
        """, ( id ,))



        dataset = db_cursor.fetchall()
        comments = []
        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])
            
            
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['created_on'], row['active'], row['profile_image_url'])
            
            comment.user = user.__dict__
            comments.append(comment.__dict__)


    return json.dumps(comments)