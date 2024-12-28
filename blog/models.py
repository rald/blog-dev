import psycopg2
from psycopg2 import sql
import hashlib

# Database setup
def init_db():
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User operations
def create_user(username, password):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
    return True

def authenticate_user(username, password):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Post operations
def get_all_posts():
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, user_id FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def get_post(post_id):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, user_id FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return post

def create_post(title, content, user_id):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)", (title, content, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_post(post_id, title, content, user_id):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s AND user_id = %s", (title, content, post_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_post(post_id, user_id):
    conn = psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s AND user_id = %s", (post_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()


