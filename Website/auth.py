# auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from .models import User
from . import db
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_no_or_email = request.form.get('regNo')
        password = request.form.get('password')

        user = User.query.filter((User.email == reg_no_or_email) | (User.reg_no == reg_no_or_email)).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role in ['Super Admin', 'admin']:
                flash(f'Successfully logged in as {user.role}', 'success')
                return redirect(url_for('views.home'))  
            elif user.role == 'student':
                flash('Successfully logged in as a student!', 'success')
                return redirect(url_for('views.home'))  
            else:
                flash('You do not have the correct privileges.', 'error')
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('/Auth/index.html')


@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullname')
        full_reg_no = request.form.get('fullRegNo')
        department = request.form.get('department')
        password = request.form.get('password')

        # Validate input values
        if not email or not full_name or not full_reg_no or not department or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.signup'))

        if len(password) < 5:
            flash('Password must be at least 5 characters long.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            return redirect(url_for('auth.signup'))

        # Create new user
        new_user = User(
            email=email,
            reg_no=full_reg_no,
            full_name=full_name,
            department=department,
            password_hash=generate_password_hash(password, method='scrypt'),
            role='student'  # set role to 'student'
        )

        # Add new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', 'success')
            login_user(new_user)
            return redirect(url_for('views.home'))  # Redirect to dashboard or home page
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            print(str(e))  # Log the error for debugging
            return redirect(url_for('auth.signup'))

    # If it's a GET request, just render the signup form
    return render_template('Auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('auth.login'))
