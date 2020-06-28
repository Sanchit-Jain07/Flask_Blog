from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from learn import db, bcrypt, mail
from flask_mail import Message
from learn.models import User, Post
from learn.users.forms import RegistrationForm, LoginForm, UpdateForm, RequestResetForm, ResetPassword
from learn.users.utils import save_picture, get_username_by_id
import os

users = Blueprint('users', __name__)


@users.route("/users")
def user_list():
	return render_template('users.html', User=User.query.all())


@users.route("/register", methods=['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		name = User.query.filter_by(username=form.username.data).first()
		if name:
			flash(f'Username already taken, try another!', 'danger')
			return redirect(url_for('users.register'))
		email = User.query.filter_by(email=form.email.data).first()
		if email:
			flash(f'Email already taken, try another!', 'danger')
			return redirect(url_for('users.register'))
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account is successfully created, you can now login!', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', form=form, title='Register')


@users.route("/login", methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash(f'{user.username} logged in successfully!', 'success')
			return redirect(url_for('main.home'))
		else:
			flash(f'Login unsuccessful, check email or password!', 'danger')
			return redirect(url_for('users.login'))
	return render_template('login.html', form=form, title='Login')

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods = ['POST', 'GET'])
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	form = UpdateForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		name = User.query.filter_by(username=form.username.data).first()
		email = User.query.filter_by(email=form.email.data).first()
		if name:
			if name != current_user:
				flash('Username is already taken, try another!', 'danger')
				return redirect(url_for('users.account'))
		if email:
			if email != current_user:
				flash('Email is already taken, try another!', 'danger')
				return redirect(url_for('users.account'))
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		print(current_user.username, current_user.email)
		flash('Profile updated successfully!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	posts = Post.query.filter_by(author=current_user).all()
	posts_dict = {}
	for post in  Post.query.all():
		posts_dict[post.id] = post.title
	return render_template('account.html', title=current_user.username, form=form ,posts=posts, image_file=image_file, posts_dict=posts_dict)



@users.route('/user/<string:username>', methods=['POST', 'GET'])
@login_required
def user_posts(username):
	print(current_user)
	user = User.query.filter_by(username=username).first_or_404()
	if user == None:
		return abort(404)
	print(user)
	posts = Post.query.filter_by(author=user).order_by(Post.date_time.desc())
	if request.method == "POST" and current_user != user:
		if request.form['submit_button'] == 'Follow':
			user.followers.append(current_user)
			print(f"{current_user} FOLLOWED {user}!")
			db.session.commit()
		elif request.form['submit_button'] == 'Unfollow':
			user.followers.remove(current_user)
			print(f'{current_user} UNFOLLOWED {user}!')
			db.session.commit()
		return redirect(url_for('users.user_posts', username=user.username))

	return render_template('user_posts.html', 
			title=user.username, user=user, posts=posts)


def send_reset_email(user):
	print(current_app.config['MAIL_DEFAULT_SENDER'])
	token = user.get_reset_token()
	msg = Message('Password Reset Request', 
		sender=current_app.config['MAIL_DEFAULT_SENDER'],
		recipients=[user.email],
		)
	msg.body = f"To reset password, visit the following link : {url_for('users.reset_token', token=token, _external=True)}"

	mail.send(msg)




@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_reset_email(user)
			flash(f'Email sent, check {form.email.data}', 'success')
			return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)



@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid/expired token!', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPassword()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pw
		db.session.commit()
		flash(f'Your password updated, you can now login!', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)

