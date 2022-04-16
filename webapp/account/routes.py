from flask import Blueprint, render_template, url_for, redirect, flash, request
from webapp import db, bcrypt
from webapp.account.utils import save_image, save_profile_image
from webapp.account.form import AccountChangeForm, RegistrationForm, LoginForm
from webapp.models import User, Post, Image
from flask_login import login_user, current_user, logout_user, login_required


account = Blueprint('account', __name__)


@account.route("/user", methods=["GET", "POST"])
def user():
    return render_template('user.html')

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

@login_required
@account.route("/account_setting", methods=["GET", "POST"])
def account_setting():
    form=AccountChangeForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.profile_image = save_profile_image(form.profile_image.data)
        db.session.commit()
        redirect(url_for('main.home'))
    return render_template('account_setting.html', user=current_user, form=form)

@account.route('/user_posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=user.id).\
        order_by(Post.time.desc()).\
        paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user, Image=Image)


@account.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    


    return render_template('profile.html', user=user)

@account.route('/user_files/<int:user_id>')
def user_files(user_id):

    return render_template('user_files.html')


@login_required
@account.route('/follow/<int:user_id>')
def follow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('error no such user exist')
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('already following')
        return redirect(url_for('account.profile', user_id=user.id))

    flash('followed')
    current_user.follow(user)
    return redirect(url_for('account.profile', user_id=user.id))


@login_required
@account.route('/unfollow/<int:user_id>')
def unfollow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('error no such user exist')
        return redirect(url_for('main.home'))
    if not current_user.is_following(user):
        flash('already not following')
        return redirect(url_for('account.profile', user_id=user.id))
    flash('unfollowed')
    current_user.unfollow(user)
    return redirect(url_for('account.profile', user_id=user.id))

@login_required
@account.route('/following/<int:user_id>')
def following(user_id):




    
    return render_template('following.html')



@account.route("/users_list", methods=["GET", "POST"])
def user_list():
    users = User.query.order_by(User.id)
    return render_template('users_list.html', users=users)