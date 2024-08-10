from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "74b34a11c22aa0df7f4c640332631d0c7eeabb46ee298907"  # Замените на сгенерированный секретный ключ
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Определяем модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Главная страница с формой регистрации
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Проверка длины пароля
        if len(password) < 6:
            flash("Пароль должен содержать не менее 6 символов.", "danger")
            return render_template(
                "register.html",
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            # return redirect(url_for("register"))

        # Проверка совпадения паролей
        if password != confirm_password:
            flash("Пароли не совпадают.", "danger")
            return render_template(
                "register.html",
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            # return redirect(url_for("register"))

        # Хеширование пароля
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Создание нового пользователя
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Вы успешно зарегистрировались!", "success")
            return redirect(url_for("register"))
        except Exception as e:
            flash("Ошибка при регистрации: возможно, email уже используется.", "danger")

    return render_template("register.html")


# Создание таблиц перед запуском приложения
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
