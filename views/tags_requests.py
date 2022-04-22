import json
import sqlite3
from models.tags import Tags


def get_all_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        ORDER BY t.label ASC
        """)

        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tags(row['id'], row['label'])
            tags.append(tag.__dict__)
    return json.dumps(tags)

def get_single_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        tag = Tags(data['id'], data['label'])


    return json.dumps(tag.__dict__)

def create_tag(new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ? );
        """, (new_tag['label'],))

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return json.dumps(new_tag)