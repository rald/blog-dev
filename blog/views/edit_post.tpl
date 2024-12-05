<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Post</title>
    <link rel="stylesheet" href="/static/css/basic.css">
</head>
<body>
    <div class="form-container">
        <h1>Edit Post</h1>
        % if error:
            <p class="error">{{error}}</p>
        % end
        <form method="POST">
            <label for="title">Title</label>
            <input id="title" name="title" type="text" value="{{post[0]}}" required>
            
            <label for="content">Content</label>
            <textarea id="content" name="content" rows="6" required>{{post[1]}}</textarea>
            
            <button type="submit">Save Changes</button>
        </form>
        <a href="/">Back to Home</a>
    </div>
</body>
</html>
