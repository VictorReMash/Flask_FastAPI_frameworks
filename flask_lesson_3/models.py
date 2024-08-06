from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pytz

db = SQLAlchemy()

local_tz = pytz.timezone("Asia/Almaty")


def get_local_time():
    return datetime.now(local_tz)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(6), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_local_time)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=get_local_time)

    def __repr__(self):
        return f"Post({self.title}, {self.content})"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=get_local_time)

    def __repr__(self):
        return f"Comment({self.content})"
