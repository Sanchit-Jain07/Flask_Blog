from flask import render_template, request, Blueprint
from learn.models import Post

main = Blueprint('main', __name__)

@main.route('/', methods=['POST','GET'])
@main.route("/home", methods=['POST','GET'])
def home():
	page = request.args.get('page',1, type=int)
	posts = Post.query.order_by(Post.date_time.desc()).paginate(per_page=4, page=page)
	return render_template('home.html', posts=posts)


