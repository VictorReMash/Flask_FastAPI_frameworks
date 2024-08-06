from flask import Flask
from flask_lesson_3.models import db, User, Post, Comment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("OK")


@app.cli.command("add-john")
def add_user():
    user = User(username="john1", email="john1@example.com")
    db.session.add(user)
    db.session.commit()
    print("John add in DB!")
