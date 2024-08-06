from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Нужно для использования flash-сообщений


# Создание базы данных и таблицы пользователей
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("register.html")


# @app.route("/base")
# def base():
#     return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Пароли не совпадают", "danger")
        return redirect(url_for("index"))

    if len(password) < 6:
        flash("Пароль должен содержать не менее 6 символов", "danger")
        return redirect(url_for("index"))

    # Хеширование пароля
    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    # Сохранение данных в базу данных
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (?, ?, ?, ?)
    """,
        (first_name, last_name, email, hashed_password),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


#
# @app.route("/login")
# def login():
#     return render_template("login.html")
#
#
# @app.route("/login", methods=["POST"])
# def login_post():
#     email = request.form["email"]
#     password = request.form["password"]
#
#     # Проверка email и пароля
#     conn = sqlite3.connect("users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
#     user = cursor.fetchone()
#     conn.close()
#
#     if user and checkpw(password.encode("utf-8"), user[0]):
#         flash("Успешный вход!", "success")
#         return redirect(url_for("base"))
#     else:
#         flash("Неверный email или пароль", "danger")
#         return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
