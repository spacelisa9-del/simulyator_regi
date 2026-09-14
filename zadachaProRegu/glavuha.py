from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = "Такой пользователь уже есть"
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            message = "Рега прошла успешно"

        conn.close()

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>симулятор регистрации</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        </head>
        <body>
            <h1>рега</h1>
            <form method="POST">
                <label>Имя:</label><br>
                <input type="text" name="username" required><br><br>
                <label>Пароль:</label><br>
                <input type="password" name="password" required><br><br>
                <button type="submit">зарегаться</button>
            </form>
            <p>{{ message }}</p>
        </body>
        </html>
    """, message=message)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)