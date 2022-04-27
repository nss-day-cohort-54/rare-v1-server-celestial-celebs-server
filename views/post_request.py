import sqlite3
import json
from models import Post, Category, User, post_tags
from models import PostTags, Tags

#def a get function to fetch a posts details for a single post
# fetch includes post, user and category
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
            u.profile_image_url,
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

        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])

        category = Category(data['category_id'], data['label'])

        post.user = user.__dict__
        post.category = category.__dict__


    return json.dumps(post.__dict__)

# get all posts with users and category
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
            u.profile_image_url,
            u.created_on,
            u.active,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            rowId = row['id']

            db_cursor.execute("""
            SELECT
                t.id,
                t.label
            FROM PostTags pt
            JOIN Tags t
                on t.id = pt.tag_id
            JOIN Posts p
                on p.id = ?
            WHERE pt.post_id = p.id
            GROUP BY t.id
            """, ( rowId, ))

            data = db_cursor.fetchall()

            tags= []

            for current_tag in data:
                tag = Tags(current_tag['id'], current_tag['label'])
                tags.append(tag.__dict__)

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['content'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            category = Category(row['category_id'], row['label'])
            post.user = user.__dict__
            post.category = category.__dict__
            post.tags = tags
            posts.append(post.__dict__)


    return json.dumps(posts)


#def a get function to delete a post and updates the post list
def delete_post(id):
     with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))
def get_all_user_posts(id):
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
            u.profile_image_url,
            u.created_on,
            u.active,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE p.user_id = ?
        """, ( id ,))



        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], 
                        row['title'], row['publication_date'], row['content'])
            
            user = User(row['id'], row['first_name'], 
                        row['last_name'], row['email'], 
                        row['bio'], row['username'], row['password'], 
                        row['profile_image_url'], row['created_on'], row['active'])
            category = Category(row['category_id'], row['label'])

            post.user = user.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)

            db_cursor.execute("""
                SELECT t.id, t.label, pt.tag_id, pt.post_id
                FROM PostTags pt
                JOIN tags t ON t.id = pt.tag_id
                WHERE pt.post_id = ?
            """, (post.id, ))

            tags = []

            tag_dataset = db_cursor.fetchall()

            for tag_row in tag_dataset:
                tags.append(tag_row['label'])

            post.tags = tags

    return json.dumps(posts)

def get_posts_by_category(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
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
            u.profile_image_url,
            u.created_on,
            u.active,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE p.category_id = ?
        """, ( category_id, ))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['content'])
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            category = Category(row['category_id'], row['label'])
            post.user = user.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)


    return json.dumps(posts)

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, content )
        VALUES
            ( ?, ?, ?, ?, ? );
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['content']))

        id = db_cursor.lastrowid

        new_post['id'] = id

        for tag in new_post['tags']:
            db_cursor.execute("""
            INSERT INTO PostTags
                (post_id, tag_id)
            VALUES
                ( ?, ? );
            """, (id, tag))

    return json.dumps(new_post)


def edit_post(id, edited_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                content = ?
        WHERE id = ?
        """, (edited_post['user_id'], edited_post['category_id'],
              edited_post['title'], edited_post['publication_date'],
              edited_post['content'], id))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


