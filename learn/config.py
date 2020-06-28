import os

class Config:
	SECRET_KEY = 'secretkeyisverysecret'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = 'testarnav17@gmail.com'

