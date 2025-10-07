from flask import Blueprint, render_template, request, redirect, flash, url_for, session

from models.prompt import Prompt

prompt_routes = Blueprint('prompt', __name__)


@prompt_routes.route('/prompt/overview', methods=['GET', 'POST'])
def prompt_overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    data = Prompt()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        prompts, total_prompts = data.get_all_prompts(page, per_page, filters)

        # Get total amount of pages
        total_pages = (total_prompts + per_page - 1) // per_page

        # Show x amount of pagination links
        start_page = max(1, page - 5)
        end_page = min(total_pages, page + 5)

        # Calculate the start and end results
        start_result = (page - 1) * per_page + 1
        end_result = min(page * per_page, total_prompts)

        return render_template('prompt_overview.html',
                               prompts=prompts, page=page,
                               per_page=per_page, total_pages=total_pages,
                               start_page=start_page, end_page=end_page,
                               start_result=start_result, end_result=end_result,
                               total_results=total_prompts)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    prompts, total_prompts = data.get_all_prompts(page, per_page, filters)

    # Get total amount of pages
    total_pages = (total_prompts + per_page - 1) // per_page

    # Show x amount of pagination links
    start_page = max(1, page - 5)
    end_page = min(total_pages, page + 5)

    # Calculate the start and end results
    start_result = (page - 1) * per_page + 1
    end_result = min(page * per_page, total_prompts)

    return render_template('prompt_overview.html',
                           prompts=prompts, page=page,
                           per_page=per_page, total_pages=total_pages,
                           start_page=start_page, end_page=end_page,
                           start_result=start_result, end_result=end_result,
                           total_results=total_prompts)


@prompt_routes.route('/prompt/<prompt_id>')
def prompt_show(prompt_id):
    data = Prompt()
    prompt = data.get_single_prompt(prompt_id)
    return render_template('prompt_show.html', prompt=prompt)


@prompt_routes.route('/prompt/create', methods=['GET', 'POST'])
def prompt_create():
    if request.method == 'POST':
        title = request.form.get('title')
        prompt = request.form.get('prompt')

        prompt_model = Prompt()
        new_prompt = prompt_model.create_prompt(title, prompt)

        # Redirect after successful form submission
        if new_prompt:
            flash("prompt met succes aangemaakt!", "success")
            return redirect(url_for('prompt.prompt_overview'))
        else:
            flash("Er is een fout opgetreden!", "danger")
            return redirect(url_for('prompt.prompt_create'))

    return render_template('prompt_create.html')


@prompt_routes.route('/prompt/update/<prompt_id>', methods=['GET', 'POST'])
def prompt_update(prompt_id):
    prompt_model = Prompt()

    if request.method == 'POST':
        title = request.form.get('title')
        prompt = request.form.get('prompt')

        prompt_model.update_prompt(prompt_id, title, prompt)

        flash("Prompt met succes bijgewerkt!", "update")
        return redirect(url_for('prompt.prompt_overview'))

    prompt = prompt_model.get_single_prompt(prompt_id)

    return render_template('prompt_update.html', prompt=prompt)


@prompt_routes.route('/prompt/delete/<prompt_id>', methods=['GET', 'POST'])
def prompt_delete(prompt_id):
    data = Prompt()

    prompt = data.get_single_prompt(prompt_id)

    if request.method == 'POST':
        data.delete_prompt(prompt_id)
        message = "User deleted successfully!", "success"
        flash("Prompt verwijderd!", "delete")
        return redirect(url_for('prompt.prompt_overview'))

    # Pass the user object to the confirmation page
    return render_template('prompt_delete_modal.html', prompt=prompt)
