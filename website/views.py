from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint("views", __name__)

# ========= USER HOME =========
@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

# ========= ADMIN HOME =========
@views.route("/")
@views.route("/admin/home")
@login_required
def adminhome():
    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()
    comments = Comment.query.all()
    return render_template("admin/home.html", user=current_user, posts=posts, users=users, likes=likes, comments=comments)

@views.route("/admin/user")
@login_required
def admin_user_view():
    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()
    comments = Comment.query.all()
    return render_template("backend/user/view_user.html", user=current_user, posts=posts, users=users, likes=likes, comments=comments)

@views.route("/admin/user/add", methods=['GET', 'POST'])
@login_required
def admin_user_add():
    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()
    comments = Comment.query.all()

    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        usertype = request.form.get("usertype")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif len(firstname) < 2:
            flash('First Name is Required.', category='error')
        elif len(lastname) < 2:
            flash('Last Name is Required.', category='error')
        elif len(username) < 2:
            flash('Username is Required.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(email=email, username=username, firstname=firstname, lastname=lastname, usertype=usertype, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("User Inserted Successfully.", category='success')
            return redirect(url_for('views.admin_user_view'))

    return render_template("backend/user/add_user.html", user=current_user)


# ========= CREATE POST =========
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', category='success') 
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

# ========= DELETE POST =========
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash("You do not gave permission do delete this post.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted Successfully', category='success')

    return redirect(url_for('views.home'))

# ========= VIEW POST =========
@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template('posts.html', user=current_user, posts=posts, username=username)

# ========= CREATE COMMENT =========
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id = post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment Posted Successfully!', category='success')
        else:
            flash('Post does not exist.', category)
        
    return redirect(url_for('views.home'))

# ========= DELETE COMMENT =========
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

# ========= LIKING POST =========
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        # flash('Post does not exist.', category='error')
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # return redirect(url_for('views.home'))
    return jsonify({"likes": len(post.likes), "liked":current_user.id in map(lambda x: x.author, post.likes)})
