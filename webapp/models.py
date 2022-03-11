from flask_login import UserMixin
from datetime import datetime
from webapp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(200), nullable=False, default="no content")
    profile_image = db.Column(db.String(100), nullable=False, default='no_image.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}, {self.email}"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    title = db.Column(db.String(100),nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Image', backref='post', lazy=True)
    
    def __repr__(self):
        return f"{self.text}, {self.images}"


class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(260), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    def __repr__(self):
        return f"{self.image}"

