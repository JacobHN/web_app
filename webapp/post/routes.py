from flask import Blueprint, render_template, current_app, redirect, url_for, flash, Flask, Request
from flask_login import current_user
from webapp.post.form import PostForm, ImageTestForm
from webapp.models import Post, Image
from webapp import db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

from webapp.post.utils import save_image

post = Blueprint('post', __name__)

@post.route("/create_post", methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        individual_post=Post(title=form.title.data, text=form.text.data, author=current_user)
        db.session.add(individual_post)
        db.session.commit()
        try:
            for image in form.image.data:
                file_name = secure_filename(save_image(image))
                img = Image(image=file_name, post=individual_post)
                db.session.add(img)
                db.session.commit()
        except:
            pass
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form)

@post.route("/update_post", methods=['GET', 'POST'])
def update_post(post_id):
    form = form
    post = Post.query.get_or_404(post_id)
    files_filenames = []

    return render_template('update_post.html', form=form)

@post.route("/post/<int:post_id>")
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    images = Image.query.filter_by(post=post)
    return render_template('post.html', post=post, images=images)



@post.route('/images_test', methods=['GET', 'POST'])
def image_test():
    form = ImageTestForm()
    individual_post = Post.query.get_or_404(1)
    if form.validate_on_submit():
         for image in form.image.data:
            file_name = secure_filename(image)
            img = Image(image=file_name, post=individual_post)
            db.session.add(img)
            db.session.commit()
    images = Image.query.order_by(Image.id)
    return render_template('image_test.html', form=form, images=images)

@post.route('/ck_editor_test', methods=['GET', 'POST'])
def ck_editor_test():
    form = PostForm()
    if form.validate_on_submit():
        individual_post=Post(title=form.title.data, text=form.text.data, author=current_user)
        db.session.add(individual_post)
        db.session.commit()
        try:
            for image in form.image.data:
                file_name = secure_filename(save_image(image))
                img = Image(image=file_name, post=individual_post)
                db.session.add(img)
                db.session.commit()
        except:
            pass
        return redirect(url_for('main.home'))

    return render_template('ck_editor_test.html', form=form)