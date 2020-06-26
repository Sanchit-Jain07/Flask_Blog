from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from learn import db
from learn.users.forms import CommentForm
from learn.models import Post, Comment, User


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
	if request.method == 'POST':
		title = request.form.get('Title')
		content = request.form.get('content')
		post = Post(title=title, content=content, user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash(f'New post named "{title}" created successfully!', 'success')
		return redirect(url_for('main.home'))
	return render_template('new_post.html')

@posts.route('/post/<int:post_id>', methods=['POST','GET'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	comment_form = CommentForm()
	if comment_form.validate_on_submit() and current_user.is_authenticated:
		comment = Comment(user_id=current_user.id, post_id=post.id, message=str(comment_form.message.data))
		db.session.add(comment)
		db.session.commit()
		flash('Your comment has been added successfully!', 'success')
		return redirect(f'/post/{str(post.id)}')
	comments = Comment.query.all()
	d = {}
	for comment in comments:
		user_id_is = comment.user_id
		user = User.query.get(user_id_is)
		d[user_id_is] = user.username
	print('d - ', d)
	return render_template('post.html', post=post, post_content=post.content, comments=comments, comment_form=comment_form, d=d)


@posts.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if current_user != post.author:
		return abort(403)
	if request.method == 'POST':
		post.title = request.form.get('Title')
		post.content = request.form.get('content')
		db.session.commit()
		flash('Your post has been updated successfully!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	return render_template('update_post.html', post=post, post_content=post.content)

@posts.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if current_user != post.author:
		return abort(403)
	flash(f'Your post named as "{ post.title }" has been deleted permanently!', 'success')
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('main.home'))

