from flask import Flask, render_template, url_for, flash, redirect, request
from flask_env import app, db, bcrypt
from flask_env.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_env.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

import secrets
import os
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        correct_pass = bcrypt.check_password_hash(user.password, form.password.data)
        if user and correct_pass:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print(request.args)
            flash(f'You have been logged in! Hello {form.email.data}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Can not login. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/img', pic_fn)
    form_picture.save(pic_path)
    return pic_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    users = User.query.all()
    # print(users)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_fn = save_picture(form.picture.data)
            print(pic_fn)
            current_user.image_file = pic_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        user = User.query.filter_by(email=current_user.email).first()
        user.image_file = current_user.image_file
        db.session.add(user)
        db.session.commit()
        flash('Updated OKE', 'success')
        print(current_user)
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Acount', users=users, image_file=image_file, form=form)
