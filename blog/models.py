import psycopg2
from psycopg2 import sql
import hashlib

# Centralized database connection
def get_connection():
    return psycopg2.connect(
        dbname="testdb",
        user="fria",
        password="alohomora",
        host="localhost",
        port="5432"
    )

# Database setup
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
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

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User operations
def create_user(username, password):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
                conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False

def authenticate_user(username, password):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
            return cursor.fetchone()

# Post operations
def get_all_posts():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title, user_id FROM posts ORDER BY id DESC")
            return cursor.fetchall()

def get_post(post_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, content, user_id FROM posts WHERE id = %s", (post_id,))
            return cursor.fetchone()

def create_post(title, content, user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)", (title, content, user_id))
            conn.commit()

def update_post(post_id, title, content, user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s AND user_id = %s", (title, content, post_id, user_id))
            conn.commit()

def delete_post(post_id, user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE id = %s AND user_id = %s", (post_id, user_id))
            conn.commit()
