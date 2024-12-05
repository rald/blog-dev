<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="/static/css/basic.css">
</head>
<body>
    <div class="form-container">
        <h1>Register</h1>
        % if error:
            <p class="error">{{error}}</p>
        % end
        <form method="POST">
            <label for="username">Username</label>
            <input id="username" name="username" type="text" required>
            
            <label for="password">Password</label>
            <input id="password" name="password" type="password" required>
            
            <button type="submit">Register</button>
        </form>
        <a href="/login">Already have an account? Login</a>
    </div>
</body>
</html>
