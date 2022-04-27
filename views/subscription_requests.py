import json
import sqlite3

from models.subscriptions import Subscription

# SQL call for subscriptions
def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM Subscriptions s
        """)

        # Initialize an empty list to hold all entry representations
        subscriptions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)
    return json.dumps(subscriptions)

def get_single_subscription(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM Subscriptions s
        WHERE s.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'], data['created_on'])


    return json.dumps(subscription.__dict__)

def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on)
        VALUES
            ( ?, ?, ? );
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on']))

        id = db_cursor.lastrowid

        new_subscription['id'] = id


    return json.dumps(new_subscription)