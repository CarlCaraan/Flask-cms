from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint("views", __name__)

# ========= USER CONTROLLER =========
# User Home

@views.route("/")
@views.route("/homepage")
def landing_page_home():
    return render_template("landing_page/home.html")

@views.route("/about")
def landing_page_about():
    return render_template("landing_page/about.html")

@views.route("/home")
@login_required
def home():
    searchbar = request.args.get('searchbar')
    if searchbar:
        posts = Post.query.filter(Post.title.contains(searchbar)).order_by(Post.date_updated.desc())
    else:
        posts = Post.query.order_by(Post.date_updated.desc())
    return render_template("user/home.html", user=current_user, posts=posts)

# POSTING JOB


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        location = request.form.get('location')
        location1 = request.form.get('location1')
        salary = request.form.get('salary')
        salary1 = request.form.get('salary1')
        level = request.form.get('level')
        specialization = request.form.get('specialization')
        experience = request.form.get('experience')
        jobtype = request.form.get('jobtype')
        qualification = request.form.get('qualification')
        qualification1 = request.form.get('qualification1')
        qualification2 = request.form.get('qualification2')
        qualification3 = request.form.get('qualification3')
        qualification4 = request.form.get('qualification4')

        if current_user.company:
            if not title:
                flash('This title field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not text:
                flash('This description field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not location:
                flash('This province field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not location1:
                flash('This city field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not level:
                flash('This career level field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not specialization:
                flash('This job specialization field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not experience:
                flash('This years of experience field is required', category='error')
                return redirect(url_for('views.create_post'))
            elif not jobtype:
                flash('This jobtype field is required', category='error')
                return redirect(url_for('views.create_post'))
            else:
                post = Post(text=text, title=title, location=location, location1=location1, salary=salary, salary1=salary1, level=level,
                            specialization=specialization, experience=experience, jobtype=jobtype, qualification=qualification, qualification1=qualification1,
                            qualification2=qualification2, qualification3=qualification3, qualification4=qualification4, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                flash('Post Created!', category='success')
                return redirect(url_for('views.home'))
        else:
            flash(
                'You must add your company in your profile before posting!', category='error')
            return redirect(url_for('views.create_post'))

    return render_template('user/post/create_post.html', user=current_user)


@views.route("/edit-post/<post_id>", methods=['GET', 'POST'])
@login_required
def user_post_edit(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form["title"]
        post.text = request.form["text"]
        post.level = request.form['level']
        post.specialization = request.form['specialization']
        post.experience = request.form['experience']
        post.jobtype = request.form['jobtype']
        post.salary = request.form['salary']
        post.salary1 = request.form['salary1']
        post.qualification = request.form['qualification']
        post.qualification1 = request.form['qualification1']
        post.qualification2 = request.form['qualification2']
        post.qualification3 = request.form['qualification3']
        post.qualification4 = request.form['qualification4']

        if not post.title:
            flash("This title field is required.", category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        elif len(post.text) < 14:
            flash(
                "This description field is required or must be greater than 2 characters.", category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        elif not post.level:
            flash('This career level field is required', category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        elif not post.specialization:
            flash('This job specialization field is required', category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        elif not post.experience:
            flash('This years of experience field is required', category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        elif not post.jobtype:
            flash('This jobtype field is required', category='error')
            return redirect(url_for('views.user_post_edit', post_id=post_id))
        else:
            db.session.commit()
            flash("Post Updated Successfully.", category='success')
            return redirect(url_for('views.user_post_edit', post_id=post_id))

    return render_template("user/post/edit_post.html", post=post, user=current_user)


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

# View Company Profile


@views.route("/posts/<company>")
@login_required
def posts(company):
    user = User.query.filter_by(company=company).first()
    if not user:
        flash('No user with that company exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template('user/posts.html', user=current_user, posts=posts, company=company)

# View Single Post


@views.route("/post/<id>")
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('No post exist!', category='error')
        return redirect(url_for('views.home'))

    return render_template('user/single_post.html', user=current_user, post=post)


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

# USER PROFILE SETTINGS AND CHANGE PASSWORD


@views.route("/user/profile")
@login_required
def user_profile_view():
    users = User.query.all()
    return render_template("user/profile/view_profile.html", user=current_user,  users=users)


@views.route("/user/profile/edit", methods=['GET', 'POST'])
@login_required
def user_profile_edit():
    user = User.query.all()

    if request.method == 'POST':
        company = request.form.get("company")

        if company != current_user.company and current_user.posts:
            flash(
                "Cannot edit company name because it is associated with some post!.", category='error')
            return redirect(url_for('views.user_profile_edit'))
        else:
            company = request.form.get("company")
            if not company:
                current_user.firstname = request.form["firstname"]
                current_user.lastname = request.form["lastname"]
                current_user.email = request.form["email"]
                current_user.username = request.form["username"]
                current_user.company = request.form["company"]
                current_user.usertype = request.form["usertype"]

                if not current_user.firstname:
                    flash("This firstname field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.lastname:
                    flash("This lastname field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.email:
                    flash("This email field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.username:
                    flash("This username field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.usertype:
                    flash("This usertype field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                else:
                    try:
                        db.session.commit()
                        flash("Profile Updated Successfully.",
                              category='success')
                        return redirect(url_for('views.user_profile_edit'))
                    except:
                        flash("email or username must be unique.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))

            elif company == current_user.company:
                current_user.firstname = request.form["firstname"]
                current_user.lastname = request.form["lastname"]
                current_user.email = request.form["email"]
                current_user.username = request.form["username"]
                current_user.company = request.form["company"]
                current_user.usertype = request.form["usertype"]

                if not current_user.firstname:
                    flash("This firstname field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.lastname:
                    flash("This lastname field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.email:
                    flash("This email field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.username:
                    flash("This username field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                elif not current_user.usertype:
                    flash("This usertype field is required.", category='error')
                    return redirect(url_for('views.user_profile_edit'))
                else:
                    try:
                        db.session.commit()
                        flash("Profile Updated Successfully.",
                              category='success')
                        return redirect(url_for('views.user_profile_edit'))
                    except:
                        flash("email or username must be unique.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))
            else:
                company = request.form.get("company")
                company_exist = User.query.filter_by(company=company).first()
                if company_exist:
                    flash('Company Name must be unique.', category='error')
                else:
                    current_user.firstname = request.form["firstname"]
                    current_user.lastname = request.form["lastname"]
                    current_user.email = request.form["email"]
                    current_user.username = request.form["username"]
                    current_user.company = request.form["company"]
                    current_user.usertype = request.form["usertype"]

                    if not current_user.firstname:
                        flash("This firstname field is required.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))
                    elif not current_user.lastname:
                        flash("This lastname field is required.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))
                    elif not current_user.email:
                        flash("This email field is required.", category='error')
                        return redirect(url_for('views.user_profile_edit'))
                    elif not current_user.username:
                        flash("This username field is required.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))
                    elif not current_user.usertype:
                        flash("This usertype field is required.",
                              category='error')
                        return redirect(url_for('views.user_profile_edit'))
                    else:
                        try:
                            db.session.commit()
                            flash("Profile Updated Successfully.",
                                  category='success')
                            return redirect(url_for('views.user_profile_edit'))
                        except:
                            flash("email or username must be unique.",
                                  category='error')
                            return redirect(url_for('views.user_profile_edit'))

    return render_template("user/profile/edit_profile.html", user=current_user)


@views.route("/user/change-password", methods=['GET', 'POST'])
@login_required
def user_profile_password():
    user = User.query.get_or_404(current_user.id)

    check_current_password = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        oldpassword = request.form["oldpassword"]

        if check_password_hash(check_current_password.password, oldpassword):
            user.password = request.form["password"]
            password2 = request.form["password2"]

            if not oldpassword:
                flash("All Fields are required.", category='error')
                return redirect(url_for('views.user_profile_password'))
            elif not password2:
                flash("All Fields are required.", category='error')
                return redirect(url_for('views.user_profile_password'))
            elif user.password != password2:
                flash("New Password dont match!.", category='error')
                return redirect(url_for('views.user_profile_password'))
            else:
                hashed_password = generate_password_hash(
                    current_user.password, method='sha256')
                update_password = User.query.filter_by(
                    id=current_user.id).update(dict(password=hashed_password))
                db.session.commit()
                flash("Password Updated Successfully.", category='success')
                return redirect(url_for('views.user_profile_password'))
        else:
            flash("Current Password Incorrect.", category='error')
            return redirect(url_for('views.user_profile_password'))

    return render_template("user/profile/edit_password.html", user=current_user)

# ========= ADMIN CONTROLLER =========
# ADMIN DASHBOARD
@views.route("/admin/home")
@login_required
def adminhome():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    posts = Post.query.all()
    likes = Like.query.all()
    users = User.query.all()
    employee = User.query.filter_by(usertype='user').all()
    admins = User.query.filter_by(usertype='admin').all()

    return render_template("admin/home.html", user=current_user, posts=posts, users=users, likes=likes, admins=admins, employee=employee)


@views.route("/admin/not-exist")
@login_required
def no_content_page():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    return render_template("admin/404.html", user=current_user)

# MANAGE USER

@views.route("/admin/user")
@login_required
def admin_user_view():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))
    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()
    return render_template("backend/user/view_user.html", user=current_user, posts=posts, users=users, likes=likes)


@views.route("/admin/user/add", methods=['GET', 'POST'])
@login_required
def admin_user_add():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    posts = Post.query.all()
    users = User.query.all()
    likes = Like.query.all()

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
            return redirect(url_for('views.admin_user_add'))
        elif username_exists:
            flash('Username is already in use.', category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not firstname:
            flash("This firstname field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not lastname:
            flash("This lastname field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not email:
            flash("This email field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not username:
            flash("This username field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not password:
            flash("This password field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        elif not usertype:
            flash("This usertype field is required.", category='error')
            return redirect(url_for('views.admin_user_add'))
        else:
            new_user = User(email=email, username=username, firstname=firstname, lastname=lastname,
                            usertype=usertype, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("User Inserted Successfully.", category='success')
            return redirect(url_for('views.admin_user_view'))

    return render_template("backend/user/add_user.html", user=current_user)


@views.route("/admin/edit-user/<user_id>", methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.email = request.form["email"]
        user.username = request.form["username"]
        user.firstname = request.form["firstname"]
        user.lastname = request.form["lastname"]
        user.usertype = request.form["usertype"]

        if not user.email:
            flash("This email field is required.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))
        elif not user.username:
            flash("This username field is required.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))
        elif not user.firstname:
            flash("This firstname field is required.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))
        elif not user.lastname:
            flash("This lastname field is required.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))
        elif not user.usertype:
            flash("This usertype field is required.", category='error')
            return redirect(url_for('views.admin_user_edit', user_id=user_id))
        else:
            try:
                db.session.commit()
                flash("User Updated Successfully.", category='success')
                return redirect(url_for('views.admin_user_view'))
            except:
                flash("Email or Username already exists.", category='error')
                return redirect(url_for('views.admin_user_edit', user_id=user_id))

    return render_template("backend/user/edit_user.html", user=user)


@views.route("/admin/delete-user/<user_id>")
@login_required
def delete_user(user_id):
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

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
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    users = User.query.all()
    return render_template("backend/profile/view_profile.html", user=current_user,  users=users)


@views.route("/admin/profile/edit", methods=['GET', 'POST'])
@login_required
def admin_profile_edit():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    user = User.query.all()

    if request.method == 'POST':
        company = request.form.get("company")

        if company != current_user.company and current_user.posts:
            flash(
                "Cannot edit company name because it is associated with some post!.", category='error')
            return redirect(url_for('views.admin_profile_edit'))
        else:
            company = request.form.get("company")
            if not company:
                current_user.firstname = request.form["firstname"]
                current_user.lastname = request.form["lastname"]
                current_user.email = request.form["email"]
                current_user.username = request.form["username"]
                current_user.company = request.form["company"]
                current_user.usertype = request.form["usertype"]

                if not current_user.firstname:
                    flash("This firstname field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.lastname:
                    flash("This lastname field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.email:
                    flash("This email field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.username:
                    flash("This username field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.usertype:
                    flash("This usertype field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                else:
                    try:
                        db.session.commit()
                        flash("Profile Updated Successfully.",
                              category='success')
                        return redirect(url_for('views.admin_profile_view'))
                    except:
                        flash("Email or Username already exists.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
            elif company == current_user.company:
                current_user.firstname = request.form["firstname"]
                current_user.lastname = request.form["lastname"]
                current_user.email = request.form["email"]
                current_user.username = request.form["username"]
                current_user.company = request.form["company"]
                current_user.usertype = request.form["usertype"]

                if not current_user.firstname:
                    flash("This firstname field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.lastname:
                    flash("This lastname field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.email:
                    flash("This email field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.username:
                    flash("This username field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                elif not current_user.usertype:
                    flash("This usertype field is required.", category='error')
                    return redirect(url_for('views.admin_profile_edit'))
                else:
                    try:
                        db.session.commit()
                        flash("Profile Updated Successfully.",
                              category='success')
                        return redirect(url_for('views.admin_profile_view'))
                    except:
                        flash("Email or Username already exists.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
            else:
                company = request.form.get("company")
                company_exist = User.query.filter_by(company=company).first()
                if company_exist:
                    flash('Company Name must be unique.', category='error')
                else:
                    current_user.firstname = request.form["firstname"]
                    current_user.lastname = request.form["lastname"]
                    current_user.email = request.form["email"]
                    current_user.username = request.form["username"]
                    current_user.company = request.form["company"]
                    current_user.usertype = request.form["usertype"]

                    if not current_user.firstname:
                        flash("This firstname field is required.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
                    elif not current_user.lastname:
                        flash("This lastname field is required.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
                    elif not current_user.email:
                        flash("This email field is required.", category='error')
                        return redirect(url_for('views.admin_profile_edit'))
                    elif not current_user.username:
                        flash("This username field is required.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
                    elif not current_user.usertype:
                        flash("This usertype field is required.",
                              category='error')
                        return redirect(url_for('views.admin_profile_edit'))
                    else:
                        try:
                            db.session.commit()
                            flash("Profile Updated Successfully.",
                                  category='success')
                            return redirect(url_for('views.admin_profile_view'))
                        except:
                            flash("Email or Username already exists.",
                                  category='error')
                            return redirect(url_for('views.admin_profile_edit'))

    return render_template("backend/profile/edit_profile.html", user=current_user)


@views.route("/admin/change-password", methods=['GET', 'POST'])
@login_required
def admin_profile_password():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    user = User.query.get_or_404(current_user.id)

    check_current_password = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        oldpassword = request.form["oldpassword"]

        if check_password_hash(check_current_password.password, oldpassword):
            user.password = request.form["password"]
            password2 = request.form["password2"]

            if not oldpassword:
                flash("All Fields are required.", category='error')
                return redirect(url_for('views.admin_profile_password'))
            elif not password2:
                flash("All Fields are required.", category='error')
                return redirect(url_for('views.admin_profile_password'))
            elif user.password != password2:
                flash("New Password dont match!.", category='error')
                return redirect(url_for('views.admin_profile_password'))
            else:
                hashed_password = generate_password_hash(
                    current_user.password, method='sha256')
                update_password = User.query.filter_by(
                    id=current_user.id).update(dict(password=hashed_password))
                db.session.commit()
                flash("Password Updated Successfully.", category='success')
                return redirect(url_for('views.admin_profile_password'))
        else:
            flash("Current Password Incorrect.", category='error')
            return redirect(url_for('views.admin_profile_password'))

    return render_template("backend/profile/edit_password.html", user=current_user)

# MANAGE POST


@views.route("/admin/post")
@login_required
def admin_post_view():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    posts = Post.query.all()
    users = User.query.all()

    return render_template("backend/post/view_post.html", user=current_user, posts=posts, users=users)


@views.route("/admin/post/add", methods=['GET', 'POST'])
@login_required
def admin_post_add():
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        location = request.form.get('location')
        location1 = request.form.get('location1')
        salary = request.form.get('salary')
        salary1 = request.form.get('salary1')
        level = request.form.get('level')
        specialization = request.form.get('specialization')
        experience = request.form.get('experience')
        jobtype = request.form.get('jobtype')
        qualification = request.form.get('qualification')
        qualification1 = request.form.get('qualification1')
        qualification2 = request.form.get('qualification2')
        qualification3 = request.form.get('qualification3')
        qualification4 = request.form.get('qualification4')

        if current_user.company:
            if not title:
                flash('This title field cannot be empty', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not text:
                flash('This description field cannot be empty', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not location:
                flash('This province field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not location1:
                flash('This city field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not level:
                flash('This career level field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not specialization:
                flash('This job specialization field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not experience:
                flash('This years of experience field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            elif not jobtype:
                flash('This jobtype field is required', category='error')
                return redirect(url_for('views.admin_post_add'))
            else:
                post = Post(text=text, title=title, location=location, location1=location1, salary=salary, salary1=salary1, level=level,
                            specialization=specialization, experience=experience, jobtype=jobtype, qualification=qualification,
                            qualification1=qualification1, qualification2=qualification2, qualification3=qualification3, qualification4=qualification4, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                flash('Post Created!', category='success')
                return redirect(url_for('views.admin_post_view'))
        else:
            flash(
                'You must add your company in your profile before posting!', category='error')
            return redirect(url_for('views.admin_post_add'))

    return render_template('backend/post/add_post.html', user=current_user)


@views.route("/admin/edit-post/<post_id>", methods=['GET', 'POST'])
@login_required
def admin_post_edit(post_id):
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form["title"]
        post.text = request.form["text"]
        post.level = request.form['level']
        post.specialization = request.form['specialization']
        post.experience = request.form['experience']
        post.jobtype = request.form['jobtype']
        post.salary = request.form['salary']
        post.salary1 = request.form['salary1']
        post.qualification = request.form['qualification']
        post.qualification1 = request.form['qualification1']
        post.qualification2 = request.form['qualification2']
        post.qualification3 = request.form['qualification3']
        post.qualification4 = request.form['qualification4']

        if not post.title:
            flash("This title field is required.", category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        elif len(post.text) < 14:
            flash(
                "This description field is required or must be greater than 2 characters.", category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        elif not post.level:
            flash('This career level field is required', category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        elif not post.specialization:
            flash('This job specialization field is required', category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        elif not post.experience:
            flash('This years of experience field is required', category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        elif not post.jobtype:
            flash('This jobtype field is required', category='error')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))
        else:
            db.session.commit()
            flash("Post Updated Successfully.", category='success')
            return redirect(url_for('views.admin_post_edit', post_id=post_id))

    return render_template("backend/post/edit_post.html", post=post, user=current_user)


@views.route("/admin/delete-post/<post_id>")
@login_required
def admin_post_delete(post_id):
    if current_user.usertype == 'user':
       return redirect(url_for('views.home'))

    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash("Post does not exist.", category='error')
        return redirect(url_for('views.admin_post_edit', post_id=post_id))
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted Successfully', category='success')
        return redirect(url_for('views.admin_post_view'))

    return render_template("backend/post/view_post.html", user=current_user)
