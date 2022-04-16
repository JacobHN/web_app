from flask_login import UserMixin
from datetime import datetime
from webapp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Follow(db.Model, UserMixin):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text)
    profile_image = db.Column(db.String(100), nullable=False, default='no_image.jpg')
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    following = db.relationship('Follow',
                foreign_keys=[Follow.follower_id],
                backref=db.backref('follower', lazy='joined'),
                lazy='dynamic',
                cascade='all, delete-orphan')
    
    follower = db.relationship('Follow',
                foreign_keys=[Follow.following_id],
                backref=db.backref('following', lazy='joined'),
                lazy='dynamic',
                cascade='all, delete-orphan')

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, following=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.following.filter_by(following_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,user):
        if user.id is None:
            return False
        return self.following.filter_by(following_id=user.id).first() is not None

    def is_follower(self,user):
        if user.id is None:
            return False
        return self.follower.filter_by(follower_id=user.id).first() is not None

    def __repr__(self):
        return f"{self.username}, {self.email}"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    title = db.Column(db.String(100),nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Image', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    
    def __repr__(self):
        return f"{self.text}, {self.images}"


class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"{self.text}"


class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(260), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"{self.image}"

