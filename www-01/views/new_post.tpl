<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Post</title>
    <link rel="stylesheet" href="/static/css/basic.css">
</head>
<body>
    <div class="form-container">
        <h1>Create New Post</h1>
        % if error:
            <p class="error">{{error}}</p>
        % end
        <form method="POST">
            <label for="title">Title</label>
            <input id="title" name="title" type="text" required>
            
            <label for="content">Content</label>
            <textarea id="content" name="content" rows="6" required></textarea>
            
            <button type="submit">Submit</button>
        </form>
        <a href="/">Back to Home</a>
    </div>
</body>
</html>
