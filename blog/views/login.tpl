<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="/static/css/basic.css">
</head>
<body>
    <div class="form-container">
        <h1>Login</h1>
        % if error:
            <p class="error">{{error}}</p>
        % end
        <form method="POST">
            <label for="username">Username</label>
            <input id="username" name="username" type="text" required>
            
            <label for="password">Password</label>
            <input id="password" name="password" type="password" required>
            
            <button type="submit">Login</button>
        </form>
        <a href="/register">Don't have an account? Register</a>
    </div>
</body>
</html>
