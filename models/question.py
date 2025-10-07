from models.database import Database


class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_total_questions(self):
        self.cursor.execute("SELECT COUNT(*) FROM questions")
        data = self.cursor.fetchone()
        return data[0] if data else 0

    def get_all_questions(self, page, per_page, filters=None, unscored_only=False):
        offset = (page - 1) * per_page

        query_get_questions = "SELECT * FROM questions WHERE 1=1"
        query_get_total_questions = "SELECT COUNT(*) FROM questions WHERE 1=1"
        params = []

        if unscored_only:
            query_get_questions += " AND (taxonomy_bloom IS NULL AND rtti IS NULL)"
            query_get_total_questions += " AND (taxonomy_bloom IS NULL AND rtti IS NULL)"

        if filters:
            if filters.get("questions_id"):
                query_get_questions += " AND questions_id LIKE ?"
                query_get_total_questions += " AND questions_id LIKE ?"
                params.append(f"%{filters['questions_id']}%")
            if filters.get("question"):
                query_get_questions += " AND question LIKE ?"
                query_get_total_questions += " AND question LIKE ?"
                params.append(f"%{filters['question']}%")
            if filters.get("vak"):
                query_get_questions += " AND vak LIKE ?"
                query_get_total_questions += " AND vak LIKE ?"
                params.append(f"%{filters['vak']}%")

        query_get_questions += " LIMIT ? OFFSET ?"
        params_get_questions = params + [per_page, offset]

        # Execute the query
        self.cursor.execute(query_get_questions, params_get_questions)
        result = self.cursor.fetchall()

        self.cursor.execute(query_get_total_questions, params)
        total_questions = self.cursor.fetchone()[0]

        return result, total_questions

    def get_single_question(self, question_id):
        self.cursor.execute("SELECT * FROM questions WHERE questions_id = ?", (question_id,))
        question = self.cursor.fetchone()
        return question

    def create_question(self, questions_id, prompts_id, users_id, question,
                        taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed,
                        answer, subject, subject_level, grade):
        self.cursor.execute(
            "INSERT into questions (questions_id,prompts_id,users_id, question, taxonomy_bloom, rtti, "
            "tax_bloom_changed, rtti_changed, answer, vak, onderwijsniveau, leerjaar, question_index) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (questions_id, prompts_id, users_id, question, taxonomy_bloom, rtti, tax_bloom_changed,
             rtti_changed, answer, subject, subject_level, grade, 0))
        self.con.commit()
        return True

    def get_handled_questions(self):
        self.cursor.execute("SELECT * FROM questions WHERE taxonomy_bloom IS NOT NULL OR rtti IS NOT NULL")
        questions = self.cursor.fetchall()
        return questions

    def get_all_users(self):
        try:
            self.cursor.execute("SELECT user_id, display_name FROM users")  # Fetch display_name instead of username
            users = self.cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

        # Update question details

    def update_question(self, questions_id, prompts_id, users_id, question,
                        taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed):
        try:
            # Fetch the existing question
            existing_question = self.get_single_question(questions_id)
            if not existing_question:
                print(f"Question with ID {questions_id} not found.")
                return None

            # Perform the update
            self.cursor.execute("""
                  UPDATE questions
                  SET prompts_id = ?, users_id = ?, question = ?, taxonomy_bloom = ?, rtti = ?, 
                      tax_bloom_changed = ?, rtti_changed = ?
                  WHERE questions_id = ?
              """, (
                prompts_id, users_id, question, taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed, questions_id))

            self.con.commit()
            print(f"Question with ID {questions_id} updated successfully.")
            return True
        except Exception as e:
            print(f"Error updating question: {e}")
            return None

    def delete_question(self, questions_id):
        self.cursor.execute("DELETE FROM questions WHERE questions_id=?", (str(questions_id),))
        self.con.commit()

    def close_connection(self):
        # Close the database connection
        self.con.close()


def call_llm_api(question_text, prompt):
    from lib.gpt.bloom_taxonomy import get_bloom_category

    taxonomy_and_explanation = get_bloom_category(question_text, prompt, "rac_test")
    return taxonomy_and_explanation
