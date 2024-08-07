from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)

app_store = Flask(__name__)
app_store.secret_key = "supersecretkey"  # Секретный ключ для сессий


@app_store.route("/")
def index():
    return render_template("index.html")


@app_store.route("/clothing")
def clothing():
    products = [
        {
            "id": 1,
            "name": "Куртка",
            "price": 5000,
            "image": "jacket.jpg",
            "description": "Теплая куртка для холодных дней.",
        },
        {
            "id": 2,
            "name": "Джинсы",
            "price": 2000,
            "image": "jeans.jpg",
            "description": "Комфортные джинсы для каждодневной носки.",
        },
    ]
    return render_template("category.html", category_name="Одежда", products=products)


@app_store.route("/shoes")
def shoes():
    products = [
        {
            "name": "Кроссовки",
            # "price": 3000,
            "image": "sneakers.jpg",
            # "description": "Стильные кроссовки для активного образа жизни.",
        },
        {
            "name": "Сапоги",
            # "price": 4000,
            "image": "boots.jpg",
            # "description": "Удобные сапоги для дождливой погоды.",
        },
        {
            "name": "Туфли",
            # "price": 3000,
            "image": "shoes.webp",
            # "description": "Стильные кроссовки для активного образа жизни.",
        },
        {
            "name": "Тапки",
            # "price": 4000,
            "image": "slippers.jpeg",
            # "description": "Удобные сапоги для дождливой погоды.",
        },
    ]
    return render_template("category.html", category_name="Обувь", products=products)


@app_store.route("/set_cookie", methods=["POST"])
def set_cookie():
    name = request.form["name"]
    email = request.form["email"]
    resp = make_response(redirect(url_for("welcome")))
    resp.set_cookie("name", name)
    resp.set_cookie("email", email)
    return resp


@app_store.route("/welcome")
def welcome():
    name = request.cookies.get("name")
    if not name:
        return redirect(url_for("index"))
    return render_template("welcome.html", name=name)


@app_store.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("name", "", expires=0)
    resp.set_cookie("email", "", expires=0)
    return resp


@app_store.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Проверка правильности логина и пароля (для примера используем фиксированные значения)
        if username == "admin" and password == "password":
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            return "Неверный логин или пароль"
    return render_template("login.html")


if __name__ == "__main__":
    app_store.run(debug=True)
