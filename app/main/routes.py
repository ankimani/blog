from flask import render_template,request, Blueprint
from app.models import Post
main=Blueprint('main', __name__)
#the Home route
@main.route("/")
@main.route('/home')
#@login_required
def index():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',title='Home',posts=posts)

#the about page route

@main.route('/about')
def about():
    
    return render_template('about.html',title='About')