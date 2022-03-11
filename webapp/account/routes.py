from flask import Blueprint, render_template, url_for, redirect, flash, request
from webapp import db, bcrypt
from webapp.account.form import RegistrationForm, LoginForm
from webapp.models import User, Post, Image
from flask_login import login_user, current_user, logout_user, login_required


account = Blueprint('account', __name__)


@account.route("/user", methods=["GET", "POST"])
def user():
    return render_template('account.html')

@account.route("/login", methods=["GET", "POST"])
def login():  
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            flash('login successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('login unsuccessful either email or password were incorrect', 'danger')
    return render_template('login.html', form=form)

@account.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@account.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'accounted created for {form.username.data}', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@account.route("/users_list", methods=["GET", "POST"])
def user_list():
    users = User.query.order_by(User.id)
    return render_template('users_list.html', users=users)