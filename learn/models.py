from datetime import datetime
from learn import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

'''NO IDEA'''
@login_manager.user_loader #convention#
def load_user(user_id):
	return User.query.get(int(user_id))
'''NO IDEA END'''

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	comments = db.relationship('Comment', backref='user',lazy='dynamic')

	followed = db.relationship(
    	'User', secondary=followers,
    	primaryjoin=(followers.c.follower_id == id),
    	secondaryjoin=(followers.c.followed_id == id),
    	backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
        )

	def get_reset_token(self, expires_sec=600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	content = db.Column(db.Text, nullable=False)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	comments = db.relationship('Comment', backref='post',lazy='dynamic')


	def __repr__(self):
		return f"Post('{self.title}', '{self.date_time}')"


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	message = db.Column(db.Text, nullable=False)
	# comment_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Comment('{self.user_id}', '{self.message}')"
