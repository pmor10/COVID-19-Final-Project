from CovidTracker.app import app 
from CovidTracker.crud.user import get_user_by_username, _get_user_password
from CovidTracker.config import SALT_SIZE

from flask import (render_template, request, session, redirect, jsonify)
import hashlib

@app.route('/login', methods=['GET'])
def display_login_form():
    """ Display log in page. """

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def validate_login_credentials():
    """ Take username and password and validate them. """

    username = request.form.get('username')
    password_entered_plain = request.form.get('password')

    result = {}
    # Does username exist?
    user = get_user_by_username(username)
    if user is None:
        result['username_found'] = False
        result['valid_login'] = None
        return jsonify(result)

    # If yes, does password match username?
    result['username_found'] = True
    salt = user.salt.encode('utf-8')

    password_entered_hash = hashlib.sha256(password_entered_plain.encode('utf-8') + salt).hexdigest()
    password_db_hash =  _get_user_password(user.user_id)

    if password_db_hash == password_entered_hash:
        result['valid_login'] = True
        # log user in by assigning their id to the session
        session['user_id'] = user.user_id

        return redirect('/user_profile')

    else:
        result['valid_login'] = False

    return jsonify(result)