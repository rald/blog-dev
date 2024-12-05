from bottle import Bottle, template, request, redirect, response, static_file
import models

app = Bottle()

# Initialize the database
models.init_db()

# Routes
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='static')

@app.route('/')
def home():
    user_id = request.get_cookie("user")
    if user_id:
        try:
            user_id = int(user_id)  # Convert to integer if it's valid
        except ValueError:
            user_id = None  # Handle invalid cookies
    posts = models.get_all_posts()
    return template('views/home.tpl', posts=posts, user_id=user_id)


@app.route('/register', method=['GET', 'POST'])
def register():
    error = None  # Default error variable
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if username and password:
            if models.create_user(username, password):
                return redirect('/login')
            else:
                error = "Username already exists or invalid input."
        else:
            error = "Both fields are required."
    return template('views/register.tpl', error=error)

@app.route('/login', method=['GET', 'POST'])
def login():
    error = None  # Default error variable
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        user = models.authenticate_user(username, password)
        if user:
            response.set_cookie("user", str(user[0]))
            return redirect('/')
        else:
            error = "Invalid username or password."
    return template('views/login.tpl', error=error)

@app.route('/logout')
def logout():
    response.delete_cookie("user")
    return redirect('/login')

@app.route('/new', method=['GET', 'POST'])
def new_post():
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')

    error = None  # Default error variable
    if request.method == 'POST':
        title = request.forms.get('title')
        content = request.forms.get('content')
        if title and content:
            models.create_post(title, content, user_id)
            return redirect('/')
        else:
            error = "All fields are required."
    return template('views/new_post.tpl', error=error)

@app.route('/edit/<post_id:int>', method=['GET', 'POST'])
def edit_post(post_id):
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')

    post = models.get_post(post_id)
    if not post or post[2] != int(user_id):
        return redirect('/')

    error = None  # Default error variable
    if request.method == 'POST':
        title = request.forms.get('title')
        content = request.forms.get('content')
        if title and content:
            models.update_post(post_id, title, content, user_id)
            return redirect('/')
        else:
            error = "All fields are required."
    return template('views/edit_post.tpl', post=post, error=error)

@app.route('/delete/<post_id:int>', method='POST')
def delete_post(post_id):
    user_id = request.get_cookie("user")
    if not user_id:
        return redirect('/login')
    models.delete_post(post_id, user_id)
    return redirect('/')

@app.route('/post/<post_id:int>')
def view_post(post_id):
    post = models.get_post(post_id)
    if post:
        return template('views/view_post.tpl', post=post)
    return "<h1>Post Not Found</h1><a href='/'>Back to Home</a>"
