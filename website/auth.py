from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


# ========= USER CONTROLLER =========
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        company = request.form.get("company")
        allcompany = User.query.all()
        if not company:
            email = request.form.get("email")
            username = request.form.get("username")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            company = request.form.get("company")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            usertype = "user"

            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()

            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password2:
                flash('Password don\'t match!', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
            elif len(firstname) < 2:
                flash('First Name is too short.', category='error')
            elif len(lastname) < 2:
                flash('Last Name is too short.', category='error')
            elif len(password1) < 6:
                flash('Password is too short.', category='error')
            elif len(email) < 4:
                flash("Email is invalid.", category='error')
            else:
                new_user = User(email=email, username=username, firstname=firstname, lastname=lastname, company=company, usertype=usertype, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
        else:
            company = request.form.get("company")
            company_exist = User.query.filter_by(company=company).first()
            if company_exist:
                flash('Company Name must be unique.', category='error')
            else:
                email = request.form.get("email")
                username = request.form.get("username")
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                company = request.form.get("company")
                password1 = request.form.get("password1")
                password2 = request.form.get("password2")
                usertype = "user"

                email_exists = User.query.filter_by(email=email).first()
                username_exists = User.query.filter_by(username=username).first()

                if email_exists:
                    flash('Email is already in use.', category='error')
                elif username_exists:
                    flash('Username is already in use.', category='error')
                elif password1 != password2:
                    flash('Password don\'t match!', category='error')
                elif len(username) < 2:
                    flash('Username is too short.', category='error')
                elif len(firstname) < 2:
                    flash('First Name is too short.', category='error')
                elif len(lastname) < 2:
                    flash('Last Name is too short.', category='error')
                elif len(password1) < 6:
                    flash('Password is too short.', category='error')
                elif len(email) < 4:
                    flash("Email is invalid.", category='error')
                else:
                    new_user = User(email=email, username=username, firstname=firstname, lastname=lastname, company=company, usertype=usertype, password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

# ========= ADMIN CONTROLLER =========
@auth.route("/admin-login", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if current_user.usertype == "admin":
                    return redirect(url_for('views.adminhome'))
                else:
                    flash('You dont have admin privilages.', category='error')
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("admin/login.html", user=current_user)


@auth.route("/admin-sign-up", methods=['GET', 'POST'])
def admin_sign_up():
    if request.method == 'POST':
        company = request.form.get("company")
        allcompany = User.query.all()
        if not company:
            email = request.form.get("email")
            username = request.form.get("username")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            company = request.form.get("company")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            usertype = "user"

            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()

            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password2:
                flash('Password don\'t match!', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
            elif len(firstname) < 2:
                flash('First Name is too short.', category='error')
            elif len(lastname) < 2:
                flash('Last Name is too short.', category='error')
            elif len(password1) < 6:
                flash('Password is too short.', category='error')
            elif len(email) < 4:
                flash("Email is invalid.", category='error')
            else:
                new_user = User(email=email, username=username, firstname=firstname, lastname=lastname,
                                company=company, usertype=usertype, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for('views.adminhome'))
        else:
            company = request.form.get("company")
            company_exist = User.query.filter_by(company=company).first()
            if company_exist:
                flash('Company Name must be unique.', category='error')
            else:
                email = request.form.get("email")
                username = request.form.get("username")
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                company = request.form.get("company")
                password1 = request.form.get("password1")
                password2 = request.form.get("password2")
                usertype = "user"

                email_exists = User.query.filter_by(email=email).first()
                username_exists = User.query.filter_by(
                    username=username).first()

                if email_exists:
                    flash('Email is already in use.', category='error')
                elif username_exists:
                    flash('Username is already in use.', category='error')
                elif password1 != password2:
                    flash('Password don\'t match!', category='error')
                elif len(username) < 2:
                    flash('Username is too short.', category='error')
                elif len(firstname) < 2:
                    flash('First Name is too short.', category='error')
                elif len(lastname) < 2:
                    flash('Last Name is too short.', category='error')
                elif len(password1) < 6:
                    flash('Password is too short.', category='error')
                elif len(email) < 4:
                    flash("Email is invalid.", category='error')
                else:
                    new_user = User(email=email, username=username, firstname=firstname, lastname=lastname,
                                    company=company, usertype=usertype, password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.adminhome'))

    return render_template("admin/signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/admin-logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("auth.adminlogin"))
