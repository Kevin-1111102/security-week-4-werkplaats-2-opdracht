from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from lib.helpers import hash_password
from models.prompt import Prompt
from models.question import Questions
from models.user import User

user_routes = Blueprint('user', __name__)


@user_routes.route('/', methods=['GET', 'POST'])
def overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    user_data = User()
    total_users = user_data.get_total_users()

    question_data = Questions()
    total_questions = question_data.get_total_questions()

    prompt_data = Prompt()
    total_prompts = prompt_data.get_total_prompts()

    return render_template('overview.html',
                           total_users=total_users,
                           total_questions=total_questions,
                           total_prompts=total_prompts)


@user_routes.route('/user/overview', methods=['GET', 'POST'])
def user_overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        users, total_users = data.get_all_users(page, per_page, filters)

        # Get total amount of pages
        total_pages = (total_users + per_page - 1) // per_page

        # Show x amount of pagination links
        start_page = max(1, page - 5)
        end_page = min(total_pages, page + 5)

        # Calculate the start and end results
        start_result = (page - 1) * per_page + 1
        end_result = min(page * per_page, total_users)

        return render_template('user_overview.html',
                               users=users, page=page,
                               per_page=per_page, total_pages=total_pages,
                               start_page=start_page, end_page=end_page,
                               start_result=start_result, end_result=end_result,
                               total_results=total_users)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    users, total_users = data.get_all_users(page, per_page, filters)

    # Get total amount of pages
    total_pages = (total_users + per_page - 1) // per_page

    # Show x amount of pagination links
    start_page = max(1, page - 5)
    end_page = min(total_pages, page + 5)

    # Calculate the start and end results
    start_result = (page - 1) * per_page + 1
    end_result = min(page * per_page, total_users)

    return render_template('user_overview.html',
                           users=users, page=page,
                           per_page=per_page, total_pages=total_pages,
                           start_page=start_page, end_page=end_page,
                           start_result=start_result, end_result=end_result,
                           total_results=total_users)


@user_routes.route('/user/<user_id>')
def user_show(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()
    user = data.get_single_user(user_id)
    return render_template('user_show.html', user=user)


@user_routes.route('/user/create', methods=['GET', 'POST'])
def user_create():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))
    if request.method == 'POST':
        # Retrieve form data
        login = request.form.get('login')
        password = request.form.get('password')
        display_name = request.form.get('display_name')
        is_admin = request.form.get('is_admin') == 'on'  # Checkbox is checked

        # Hash the password before saving
        hashed_password = hash_password(password)

        # Process the form data (save to database, etc.)
        user_model = User()
        new_user = user_model.create_user(login, hashed_password, display_name, is_admin)

        # Redirect after successful form submission
        if new_user:
            flash("Gebruiker met succes aangemaakt!", "success")
            return redirect(url_for('user.user_overview'))
        else:
            flash("Er is een fout opgetreden!", "danger")
            return redirect(url_for('user.user_create'))

    return render_template('user_create.html')


@user_routes.route('/user/update/<user_id>', methods=['GET', 'POST'])
def user_update(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    user_model = User()

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        display_name = request.form.get('display_name')
        is_admin = request.form.get('is_admin') == 'on'

        # Hash the password if provided
        hashed_password = hash_password(password) if password else None
        user_model.update_user(user_id, login, hashed_password, display_name, is_admin)

        # Optionally, add a success message
        flash("Gebruiker met succes bijgewerkt!", "update")

        # Close the connection after updating the user
        user_model.close_connection()

        return redirect(url_for('user.user_overview'))

    # For GET request: Show the form pre-filled with user data
    user = user_model.get_single_user(user_id)

    # Close the connection after fetching user data
    user_model.close_connection()

    return render_template('user_update.html', user=user)


@user_routes.route('/user/delete/<user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()

    # Fetch user by ID
    user = data.get_single_user(user_id)  # This should return the user object with `user_username` and `user_id`

    if request.method == 'POST':
        # Handle deletion
        data.delete_user(user_id)
        flash("Gebruiker verwijderd!", "delete")
        return redirect(url_for('user.user_overview'))

    # Pass the user object to the confirmation page
    return render_template('user_delete_modal.html', user=user)
