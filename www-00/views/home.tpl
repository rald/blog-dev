<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Blog</title>
    <link rel="stylesheet" href="/static/css/basic.css">
</head>
<body>
    <h1>Simple Blog</h1>
    <p>Welcome! <a href="/logout" class="logout">Logout</a></p>
    <a href="/new" class="new-post">Create New Post</a>
    <ul>
        % for id, title, post_user_id in posts:
            <li>
                <a href="/post/{{id}}">{{title}}</a>
                % if post_user_id == int(user_id):
                    <form action="/edit/{{id}}" method="GET">
                        <button type="submit">Edit</button>
                    </form>
                    <form action="/delete/{{id}}" method="POST" onsubmit="return confirm('Are you sure you want to delete this post?');">
                        <button type="submit">Delete</button>
                    </form>
                % end
            </li>
        % end
    </ul>
</body>
</html>
