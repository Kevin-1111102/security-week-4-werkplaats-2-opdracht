from flask import Blueprint, render_template, request, redirect, url_for, session

from lib.helpers import hash_password
from models.user import User

login_routes = Blueprint('login', __name__)


@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" in session:
        return redirect(url_for('question.question_overview'))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User()
            hashed_password = hash_password(password)
            is_checked = user.check_pass(username, hashed_password)

            if is_checked:

                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user.get_user_by_name(username)['user_id']
                session['is_admin'] = user.get_user_by_name(username)['is_admin']
                return redirect(url_for('question.question_overview'))
            else:
                return render_template('login.html')

        return render_template('login.html')


@login_routes.route('/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('username', None)
    session.pop('is_admin', None)
    session.clear()
    return redirect(url_for('login.login'))
