import os
import secrets
from PIL import Image
from flask import url_for, current_app
from learn.models import User


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	
	# output_size = (128, 128)
	# i = Image.open(form_picture)
	# i.thumbnail(output_size)
	form_picture.save(picture_path)

	return picture_fn

def get_username_by_id(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user:
		return user.username
	return None