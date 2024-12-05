import sqlite3
import hashlib

# Database setup
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User operations
def create_user(username, password):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def authenticate_user(username, password):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

# Post operations
def get_all_posts():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, user_id FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_post(post_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, user_id FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

def create_post(title, content, user_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)", (title, content, user_id))
    conn.commit()
    conn.close()

def update_post(post_id, title, content, user_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET title = ?, content = ? WHERE id = ? AND user_id = ?", (title, content, post_id, user_id))
    conn.commit()
    conn.close()

def delete_post(post_id, user_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
    conn.commit()
    conn.close()
