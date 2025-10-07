import json
import logging
import os

from flask import Flask

from models.database import Database

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app setup
app = Flask(__name__)

# Database path
DB_PATH = os.path.abspath('databases/database.db')  # Use an absolute path for reliability


def process_json(file):
    # Load the JSON file
    try:
        json_data = json.load(file)
    except json.JSONDecodeError as e:
        return {"error": f"ongeldige JSON format: {e}"}

    # Validate JSON content
    if isinstance(json_data, dict):
        json_data = [json_data]  # Wrap in a list for consistent processing

    if not json_data:
        return {"error": "Uploaded JSON is leeg of ongelding."}

    # Initialize database connection
    db = Database(DB_PATH)
    cursor, connection = db.connect_db()

    error_messages = []

    try:
        for question in json_data:
            try:
                # Extract question data
                question_id = question.get('question_id')
                question_text = question.get('question')
                answer = question.get('answer', '')
                subject = question.get('vak', '')
                educational_level = question.get('onderwijsniveau', '')
                grade = question.get('leerjaar')
                question_index = question.get('question_index')
                taxonomy_bloom = question.get('taxonomy_bloom')
                rtti = question.get('rtti')

                # Validate required fields
                if not question_id or not question_text:
                    raise ValueError("Missing required fields 'question_id' or 'question'.")

                # Insert into database
                sql = '''
                    INSERT INTO questions 
                    (questions_id, prompts_id, users_id, question, answer, vak, onderwijsniveau, 
                    leerjaar, question_index, taxonomy_bloom, rtti) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                val = (
                    question_id,  # questions_id
                    0,  # prompts_id
                    '',  # users_id
                    question_text,
                    answer,
                    subject,
                    educational_level,
                    grade,
                    question_index,
                    taxonomy_bloom,
                    rtti
                )
                cursor.execute(sql, val)

            except Exception:
                # Log individual question errors
                error_messages.append(f"Error id is niet uniek {question.get('question_id')}")
                continue

        # Commit all changes after processing
        connection.commit()

    except Exception as e:
        # Handle general database errors
        return {"error": f"Database insertion error: {e}"}

    finally:
        # Ensure the database connection is properly closed
        db.close_connection()

    # Return errors if any
    if error_messages:
        return {"error": "\n".join(error_messages)}

    # Return success message if no errors occurred
    return {"success": "JSON file is geüpload."}
