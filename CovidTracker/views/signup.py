from CovidTracker.app import app, db
from CovidTracker.crud.user import get_user_by_username, create_user, get_user_by_username
from CovidTracker.config import SALT_SIZE 

import hashlib 
import binascii
import os 

from flask import (render_template, request, flash, session, redirect)

#======================= Signup =====================#
@app.route('/signup', methods=['GET'])
def display_signup_form():
    """ Display sign Up page. """

    return render_template('/signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Sign up new user and then redirect to homepage. """

    email = request.form.get('email')
    username = request.form.get('username')

    if username == get_user_by_username(username):
        error = 'User already exists.'
        return render_template('signup.html', error=error)
    else:
        flash('User is available.')

    password = request.form.get('password1')
    salt = binascii.hexlify(os.urandom(SALT_SIZE))
    password_hash = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()

    create_user(username, email, password_hash, salt=salt.decode('utf-8'))
    db_user = get_user_by_username(username)
    session['user_id'] = db_user.user_id
    flash(f'{username} successfully signed up.')
    return redirect('/')