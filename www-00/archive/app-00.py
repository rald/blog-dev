from bottle import Bottle, run, template, request, redirect
import sqlite3

# Initialize the Bottle application
app = Bottle()

# Database setup
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Route: Home (list all blog posts)
@app.route('/')
def home():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()
    return template("""
        <h1>Simple Blog</h1>
        <a href="/new">Create New Post</a>
        <ul>
            % for id, title in posts:
                <li><a href="/post/{{id}}">{{title}}</a></li>
            % end
        </ul>
    """, posts=posts)

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

# Route: Create a new blog post
@app.route('/new', method=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.forms.get('title')
        content = request.forms.get('content')
        if title and content:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
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

# Initialize the database and start the server
if __name__ == '__main__':
    init_db()
    run(app, host='localhost', port=8000, debug=True)
