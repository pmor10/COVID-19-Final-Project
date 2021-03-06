from CovidTracker.app import app 
from flask import (session, redirect, flash)

@app.route('/logout')
def logout():
    """ Logout the current logged in user. """
    if 'user_id' in session:
        flash(f"{session['user_id']} successfully logged out.")
        del session['user_id']

    return redirect('/')