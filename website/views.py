from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint("views", __name__)

# ========= USER CONTROLLER =========
# User Home
@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

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

# User View Post
@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template('posts.html', user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment Posted Successfully!', category='success')
        else:
            flash('Post does not exist.', category)

    return redirect(url_for('views.home'))

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

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

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
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

# ========= ADMIN CONTROLLER =========
# ADMIN DASHBOARD
@views.route("/")
@views.route("/admin/home")
@login_required
def adminhome():
    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()
    comments = Comment.query.all()
    return render_template("admin/home.html", user=current_user, posts=posts, users=users, likes=likes, comments=comments)

@views.route("/admin/not-exist")
@login_required
def no_content_page():

    return render_template("admin/404.html", user=current_user)

# MANAGE USER
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
            new_user = User(email=email, username=username, firstname=firstname, lastname=lastname,
                            usertype=usertype, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("User Inserted Successfully.", category='success')
            return redirect(url_for('views.admin_user_view'))

    return render_template("backend/user/add_user.html", user=current_user)

@views.route("/edit-user/<user_id>", methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.email = request.form["email"]
        user.username = request.form["username"]
        user.firstname = request.form["firstname"]
        user.lastname = request.form["lastname"]
        user.usertype = request.form["usertype"]

        try:
            db.session.commit()
            flash("User Updated Successfully.", category='success')
            return redirect(url_for('views.admin_user_view'))
        except:
            flash("Email or Username already exists.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))

    return render_template("backend/user/edit_user.html", user=user)

@views.route("/delete-user/<user_id>")
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User does not exist.', category='error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted Successfully.', category='success')

    return redirect(url_for('views.admin_user_view'))

# MANAGE PROFILE
@views.route("/admin/profile")
@login_required
def admin_profile_view():
    users = User.query.all()
    return render_template("backend/profile/view_profile.html", user=current_user,  users=users)

@views.route("/admin/profile/edit", methods=['GET', 'POST'])
@login_required
def admin_profile_edit():
    user = User.query.all()

    if request.method == 'POST':
        current_user.email = request.form["email"]
        current_user.username = request.form["username"]
        current_user.firstname = request.form["firstname"]
        current_user.lastname = request.form["lastname"]
        current_user.usertype = request.form["usertype"]

        try:
            db.session.commit()
            flash("Profile Updated Successfully.", category='success')
            return redirect(url_for('views.admin_profile_view'))
        except:
            flash("Email or Username already exists.", category='error')
            return redirect(url_for('views.admin_profile_edit'))

    return render_template("backend/profile/edit_profile.html", user=current_user)

@views.route("/admin/change-password", methods=['GET', 'POST'])
@login_required
def admin_profile_password():
    user_id = current_user.id
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        oldpassword = request.form["oldpassword"]
        user.password = request.form["password"]
        password2 = request.form["password2"]

        db.session.commit()
        flash("Password Updated Successfully.", category='success')
        return redirect(url_for('views.admin_profile_password'))
         

      
    return render_template("backend/profile/edit_password.html", user=current_user)
