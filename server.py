# import crud
from flask import (Flask, render_template, request, flash, session, Blueprint, redirect)
from model import connect_to_db
from jinja2 import StrictUndefined
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

bcrypt = Bcrypt(app)

@app.route('/')
def landingpage():
    """View Landing Page"""

    return render_template('index.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port="8080")