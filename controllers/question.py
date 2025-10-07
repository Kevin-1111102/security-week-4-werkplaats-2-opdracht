import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file

from models.prompt import Prompt
from models.question import Questions, call_llm_api
from models.question_extraction import process_json

question_routes = Blueprint('question', __name__)


def create_export_file():
    data = Questions()
    all_questions = data.get_handled_questions()
    file_path = "export_files/questions_export.json"

    with open(file_path, "w") as f:
        for question in all_questions:
            f.write(json.dumps(dict(question)) + ",")
            data.delete_question(question["questions_id"])
        f.close()


@question_routes.route('/question/download')
def export_questions():
    create_export_file()
    file_path = "export_files/questions_export.json"
    return send_file(file_path, as_attachment=True)


@question_routes.route('/question/question_indexing')
def question_indexing():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    return "question_indexing"


@question_routes.route('/question/create', methods=['GET', 'POST'])
def create_question():
    if request.method == "POST":
        try:
            questions_id = request.form.get('questions_id')
            prompts_id = -1
            users_id = session["user_id"]
            question = request.form.get('question')
            taxonomy_bloom = None
            rtti = None
            taxonomy_bloom_changed = 0
            rtti_changed = 0
            answer = request.form.get('answer')
            subject = request.form.get('subject')
            subject_level = request.form.get('subject_level')
            grade = request.form.get('grade')

            data = Questions()
            data.create_question(questions_id, prompts_id, users_id, question, taxonomy_bloom,
                                 rtti, taxonomy_bloom_changed, rtti_changed,
                                 answer, subject, subject_level, grade)

            flash("Vraag met succes aangemaakt!", "success")
            return redirect(url_for("question.question_overview"))
        except Exception as e:
            flash("Er is een fout opgetreden!", "danger")
            return redirect(url_for("question.create_question"))

    return render_template('question_create.html')


@question_routes.route('/question/overview', methods=['GET', 'POST'])
def question_overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    data = Questions()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        questions, total_questions = data.get_all_questions(page, per_page, filters)

        # Get total amount of pages
        total_pages = (total_questions + per_page - 1) // per_page

        # Show x amount of pagination links
        start_page = max(1, page - 5)
        end_page = min(total_pages, page + 5)

        # Calculate the start and end results
        start_result = (page - 1) * per_page + 1
        end_result = min(page * per_page, total_questions)

        return render_template('question_overview.html',
                               questions=questions, page=page,
                               per_page=per_page, total_pages=total_pages,
                               start_page=start_page, end_page=end_page,
                               start_result=start_result, end_result=end_result
                               )

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    questions, total_questions = data.get_all_questions(page, per_page, filters)

    # Get total amount of pages
    total_pages = (total_questions + per_page - 1) // per_page

    # Show x amount of pagination links
    start_page = max(1, page - 4)
    end_page = min(total_pages, page + 4)

    # Calculate the start and end results
    start_result = (page - 1) * per_page + 1
    end_result = min(page * per_page, total_questions)

    return render_template('question_overview.html',
                           questions=questions, page=page,
                           per_page=per_page, total_pages=total_pages,
                           start_page=start_page, end_page=end_page,
                           start_result=start_result, end_result=end_result,
                           total_results=total_questions)


@question_routes.route('/question/<question_id>')
def question_show(question_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    data = Questions()
    question = data.get_single_question(question_id)

    prompt = Prompt()
    prompts = prompt.get_prompts()

    # Get the generated prompts for the specific questions
    proposal = session.get('generated_proposals', {}).get(question_id)

    return render_template('question_show.html', question=question, prompts=prompts, proposal=proposal)


@question_routes.route('/question/update_taxonomy/<question_id>', methods=['POST'])
def update_taxonomy(question_id):
    selected_taxonomy = request.form.get('taxonomy_bloom')
    users_id = session.get('user_id')
    data = Questions()

    try:
        # Update the taxonomy in the database
        data.cursor.execute("""
            UPDATE questions
            SET taxonomy_bloom = ?, users_id = ?
            WHERE questions_id = ?
        """, (selected_taxonomy, users_id, question_id))
        data.con.commit()
        flash("Taxonomie succesvol bijgewerkt!", "success")

        # Determine the next question ID
        data.cursor.execute("""
            SELECT questions_id
            FROM questions
            WHERE questions_id > ?
            ORDER BY questions_id ASC
            LIMIT 1
        """, (question_id,))
        next_question = data.cursor.fetchone()

        # Redirect to the next question or the overview if no more questions
        if next_question:
            return redirect(url_for('question.question_show', question_id=next_question[0]))
        else:
            flash("Geen volgende vraag beschikbaar!", "info")
            return redirect(url_for('question.question_overview'))
    except Exception as e:
        flash(f"Fout bij het bijwerken van de taxonomie: {e}", "danger")
        return redirect(url_for('question.question_show', question_id=question_id))
    finally:
        data.close_connection()


@question_routes.route('/question/delete/<question_id>', methods=['GET', 'POST'])
def question_delete(question_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = Questions()

    question = data.get_single_question(question_id)

    if request.method == 'POST':
        data.delete_question(question_id)
        flash("Vraag verwijderd!", "delete")
        return redirect(url_for('question.question_overview'))

    return render_template('question_delete_modal.html', question=question)


@question_routes.route('/question/upload')
def upload_page():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))
    return render_template('upload.html')


@question_routes.route('/question/upload', methods=['POST'])
def upload_json():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    result = process_json(file)

    if "error" in result:
        return render_template('upload.html', result=result)
    return render_template('upload.html', result=result)


@question_routes.route('/question/update/<questions_id>', methods=['GET', 'POST'])
def question_update(questions_id):
    # Ensure the user is logged in
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    question_model = Questions()

    if request.method == 'POST':
        # Collect data from the form
        prompts_id = request.form.get('prompts_id')
        users_id = request.form.get('users_id')  # Capture the new users_id from dropdown
        question = request.form.get('question')
        taxonomy_bloom = request.form.get('taxonomy_bloom')
        rtti = request.form.get('rtti')
        tax_bloom_changed = request.form.get('tax_bloom_changed') == 'on'
        rtti_changed = request.form.get('rtti_changed') == 'on'

        # Update the question in the database
        question_model.update_question(
            questions_id, prompts_id, users_id, question,
            taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed
        )

        flash("Vraag met succes bijgewerkt!", "update")

        # Close the database connection
        question_model.close_connection()

        return redirect(url_for('question.question_overview'))

    question = question_model.get_single_question(questions_id)
    users = question_model.get_all_users()  # Fetch all users for dropdown

    # Close the database connection after fetching the data
    question_model.close_connection()

    return render_template('question_update.html', question=question, users=users)


@question_routes.route('/question/generate_proposal/<question_id>', methods=['POST'])
def generate_proposal(question_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    data = Questions()
    question = data.get_single_question(question_id)

    if not question:
        flash("Question not found.", "danger")
        return redirect(url_for('question.question_show', question_id=question_id))

    prompt_id = request.form.get('prompt_id')
    prompt_model = Prompt()
    selected_prompt = prompt_model.get_single_prompt(prompt_id)

    if not selected_prompt:
        flash("Prompt not found.", "danger")
        return redirect(url_for('question.question_show', question_id=question_id))

    proposal = call_llm_api(question['question'], selected_prompt['prompt'])

    if proposal:
        # Sla de prompt op in een dictionary met de vraag-ID als sleutel
        if 'generated_proposals' not in session:
            session['generated_proposals'] = {}
        session['generated_proposals'][question_id] = proposal
        session.modified = True  # Zorg ervoor dat de sessie wordt bijgewerkt
        flash("Proposal generated successfully!", "success")
    else:
        flash("Failed to generate proposal.", "danger")

    return redirect(url_for('question.question_show', question_id=question_id))
