import os

class Config:
	SECRET_KEY = 'secretkeyisverysecret'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = 'testarnav17@gmail.com'
	MAIL_PASSWORD = 'testmenow17'
	MAIL_DEFAULT_SENDER = 'testarnav17@gmail.com'

