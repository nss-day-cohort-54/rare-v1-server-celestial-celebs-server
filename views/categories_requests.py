import json
import sqlite3

from models.category import Category

# SQL call for categories
def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        """)

        # Initialize an empty list to hold all entry representations
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)
    return json.dumps(categories)

def get_single_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Category c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        category = Category(data['id'], data['label'])


    return json.dumps(category.__dict__)

def create_category(new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            ( label )
        VALUES
            ( ? );
        """, (new_category['label'],))

        id = db_cursor.lastrowid

        new_category['id'] = id

    return json.dumps(new_category)