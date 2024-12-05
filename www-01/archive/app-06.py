from bottle import Bottle, run, template, request, redirect, response
import sqlite3
import hashlib

# Initialize the Bottle application
app = Bottle()

# Database setup
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    # Create users table
    # Create posts table
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

# Route: Register
@app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if username and password:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                               (username, hash_password(password)))
                conn.commit()
                conn.close()
                return redirect('/login')
            except sqlite3.IntegrityError:
                return "<h1>Username already exists</h1><a href='/register'>Try Again</a>"
        else:
            return "<h1>Both fields are required</h1><a href='/register'>Try Again</a>"

    return template("""
        <h1>Register</h1>
        <form method="POST">
            <label>Username: <input name="username" type="text"></label><br>
            <label>Password: <input name="password" type="password"></label><br>
            <button type="submit">Register</button>
        </form>
        <a href="/login">Login</a>
    """)

# Route: Login
@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?",
                       (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        if user:
            response.set_cookie("user", str(user[0]))
            return redirect('/')
        else:
            return "<h1>Invalid username or password</h1><a href='/login'>Try Again</a>"

    return template("""
        <h1>Login</h1>
        <form method="POST">
            <label>Username: <input name="username" type="text"></label><br>
            <label>Password: <input name="password" type="password"></label><br>
            <button type="submit">Login</button>
        </form>
        <a href="/register">Register</a>
    """)

# Route: Home (list all blog posts sorted by ID in reverse)
@app.route('/')
def home():
    user_id = request.get_cookie("user")
    if user_id:
        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, user_id FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
        conn.close()
        return template("""
            <h1>Simple Blog</h1>
            <p>Welcome! <a href="/logout">Logout</a></p>
            <a href="/new">Create New Post</a>
            <ul>
                % for id, title, post_user_id in posts:
                    <li>
                        <a href="/post/{{id}}">{{title}}</a>
                        % if post_user_id == int(user_id):
                            <form action="/edit/{{id}}" method="GET" style="display:inline;">
                                <button type="submit">Edit</button>
                            </form>
                            <form action="/delete/{{id}}" method="POST" style="display:inline;" onsubmit="return confirm('Are you sure you want to delete this post?');">
                                <button type="submit">Delete</button>
                            </form>
                        % end
                    </li>
                % end
            </ul>
        """, posts=posts, user_id=user_id)
    else:
        return redirect('/login')

# Route: Logout
@app.route('/logout')
def logout():
    response.delete_cookie("user")
    return redirect('/login')

# Route: Create a new blog post
@app.route('/new', method=['GET', 'POST'])
def new_post():
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')

    if request.method == 'POST':
        title = request.forms.get('title')
        content = request.forms.get('content')
        if title and content:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                (title, content, user_id)
            )
            conn.commit()
            conn.close()
            return redirect('/')
        else:
            return "<h1>Both Title and Content are required!</h1><a href='/new'>Try Again</a>"

    return template("""
        <h1>Create New Post</h1>
        <form method="POST">
            <label>Title: <input name="title" type="text"></label><br>
            <label>Content: <textarea name="content"></textarea></label><br>
            <button type="submit">Submit</button>
        </form>
        <a href="/">Back to Home</a>
    """)

# Route: Delete a blog post
@app.route('/delete/<post_id:int>', method='POST')
def delete_post(post_id):
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    # Check if the post belongs to the logged-in user
    cursor.execute("SELECT id FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
    post = cursor.fetchone()
    if post:
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn.close()
        return "<h1>You are not authorized to delete this post</h1><a href='/'>Back to Home</a>"
# Route: View a single blog post
@app.route('/post/<post_id:int>')
def view_post(post_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    if post:
        return template("""
            <h1>{{post[0]}}</h1>
            <p>{{post[1]}}</p>
            <a href="/">Back to Home</a>
        """, post=post)
    else:
        return "<h1>Post Not Found</h1><a href='/'>Back to Home</a>"

# Route: Edit a single blog post
@app.route('/edit/<post_id:int>', method=['GET', 'POST'])
def edit_post(post_id):
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    # Check if the post belongs to the logged-in user
    cursor.execute("SELECT title, content FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
    post = cursor.fetchone()

    if not post:
        conn.close()
        return "<h1>You are not authorized to edit this post</h1><a href='/'>Back to Home</a>"

    message = None  # Placeholder for feedback messages

    if request.method == 'POST':
        title = request.forms.get('title')
        content = request.forms.get('content')
        if title and content:
            cursor.execute(
                "UPDATE posts SET title = ?, content = ? WHERE id = ? AND user_id = ?",
                (title, content, post_id, user_id)
            )
            conn.commit()
            message = "Post updated successfully!"
            # Reload the updated post data
            cursor.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()
        else:
            message = "Both Title and Content are required!"

    conn.close()
    return template("""
        <h1>Edit Post</h1>
        % if message:
            <p style="color: green;">{{message}}</p>
        % end
        <form method="POST">
            <label>Title: <input name="title" type="text" value="{{post[0]}}"></label><br>
            <label>Content: <textarea name="content">{{post[1]}}</textarea></label><br>
            <button type="submit">Save Changes</button>
        </form>
        <a href="/">Back to Home</a>
    """, post=post, message=message)

# Initialize the database and start the server
if __name__ == '__main__':
    init_db()
    run(app, host='localhost', port=14344, debug=True)
