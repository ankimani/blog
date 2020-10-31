from flask import render_template,url_for, flash, redirect,request,abort,Blueprint,current_app
from app import db,mail
from app.posts.forms import PostForm
from app.models import Post
from flask_login import login_user, current_user,logout_user,login_required

posts=Blueprint('posts',__name__)

@posts.route('/new/post',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Created Successfully",'success')
        return redirect(url_for('main.index'))
    return render_template('createpost.html',title='Post',
        form=form,legend='Create New Article')
@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):

    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)
@posts.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Article has been Updated Successfuly','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':    
        form.title.data=post.title
        form.content.data=post.content
    return render_template('createpost.html',title='Update Post',form=form,
                    legend='Update Article')   

@posts.route('/post/<int:post_id>/delete',methods=['POST','GET'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)   
    db.session.delete(post)   
    db.session.commit() 
    flash('Article has been Deleted Successfuly','success')
    return redirect(url_for('main.index'))                 
